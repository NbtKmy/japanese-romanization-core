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
_HATSUONBIN_MARKER = "撥音便"


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
        had_pending_sokuon = [
            kr is not None and kr.pending_sokuon for kr in pre_context
        ]
        had_pending_syllabic_n = [
            kr is not None and kr.pending_syllabic_n for kr in pre_context
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

            # Sokuon always fuses with a real next token: っ physically
            # borrows the next mora's initial consonant, so the two are
            # never independent words (only verb conjugation forms like
            # 促音便 end in っ). Moraic ん is different -- ordinary complete
            # words routinely end in ん (日本, 缶, ...) and are followed by
            # a particle with a normal space ("Nippon wa", "kan o"), so
            # fusion is only correct for the same kind of bound
            # conjugational form (撥音便 verb stems, e.g. 読ん+だ -> yonda).
            next_kr = resolved[i + 1] if i + 1 < len(resolved) else None
            fuses_with_next = next_kr is not None and (
                had_pending_sokuon[i]
                or (had_pending_syllabic_n[i] and _is_hatsuonbin(token))
            )

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


def _is_hatsuonbin(token: Token) -> bool:
    return (
        token.conjugation_form is not None
        and _HATSUONBIN_MARKER in token.conjugation_form
    )


def _particle_override(token: Token) -> str | None:
    if not token.pos or token.pos[0] != _PARTICLE_POS:
        return None
    if token.kana is None or token.pronunciation is None:
        return None
    return _PARTICLE_OVERRIDES.get((token.kana, token.pronunciation))
