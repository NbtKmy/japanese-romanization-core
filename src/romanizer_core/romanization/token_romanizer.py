"""Orchestrates KanaRomanizer -> ContextResolver -> LongVowelResolver and
applies は/へ/を particle overrides (kana_romanizer_spec.md Part XIII).
"""

from typing import Sequence

from ..kana.romanizer import KanaRomanizer
from ..models.kana_romanization import KanaRomanization
from ..models.romanized_token import RomanizedToken
from ..models.token import Token
from .context_resolver import ContextResolver
from .long_vowel_resolver import LongVowelResolver

_PARTICLE_POS = "助詞"
_PARTICLE_OVERRIDES: dict[tuple[str, str], str] = {
    ("ハ", "ワ"): "wa",
    ("ヘ", "エ"): "e",
    ("ヲ", "オ"): "o",
}


class TokenRomanizer:
    def __init__(
        self,
        kana_romanizer: KanaRomanizer,
        context_resolver: ContextResolver,
        long_vowel_resolver: LongVowelResolver,
    ) -> None:
        self._kana_romanizer = kana_romanizer
        self._context_resolver = context_resolver
        self._long_vowel_resolver = long_vowel_resolver

    def romanize(self, tokens: Sequence[Token]) -> tuple[RomanizedToken, ...]:
        initial = [
            _initial_romanization(token, self._kana_romanizer) for token in tokens
        ]
        pre_context = [kr for kr, _source in initial]
        had_pending = [
            kr is not None and (kr.pending_sokuon or kr.pending_syllabic_n)
            for kr in pre_context
        ]

        resolved = self._context_resolver.resolve(pre_context)

        results: list[RomanizedToken] = []
        for i, token in enumerate(tokens):
            kr = resolved[i]
            source = initial[i][1]

            if kr is None:
                romaji = _literal_text(token, source)
            else:
                kr = self._long_vowel_resolver.resolve(
                    token=token, kana_romanization=kr
                )
                override = _particle_override(token)
                if override is not None:
                    romaji = override
                    source = "pronunciation"
                else:
                    romaji = kr.text

            next_kr = resolved[i + 1] if i + 1 < len(resolved) else None
            fuses_with_next = had_pending[i] and next_kr is not None

            results.append(
                RomanizedToken(
                    token_id=token.id,
                    romaji=romaji,
                    source=source,
                    fuses_with_next=fuses_with_next,
                )
            )

        return tuple(results)


def _initial_romanization(
    token: Token, kana_romanizer: KanaRomanizer
) -> tuple[KanaRomanization | None, str]:
    if token.kana is not None:
        return kana_romanizer.romanize(token.kana), "kana"
    if token.pronunciation is not None:
        return kana_romanizer.romanize(token.pronunciation), "pronunciation"
    if token.orth is not None:
        return None, "orth"
    return None, "surface"


def _literal_text(token: Token, source: str) -> str:
    if source == "orth":
        assert token.orth is not None
        return token.orth
    return token.surface


def _particle_override(token: Token) -> str | None:
    if not token.pos or token.pos[0] != _PARTICLE_POS:
        return None
    if token.kana is None or token.pronunciation is None:
        return None
    return _PARTICLE_OVERRIDES.get((token.kana, token.pronunciation))
