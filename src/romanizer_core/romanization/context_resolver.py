"""Resolves cross-token っ/ん pending state (kana_romanizer_spec.md Part VI/VII)."""

from dataclasses import replace
from typing import Sequence

from ..kana.romanizer import sokuon_prefix
from ..models.kana_romanization import KanaRomanization

_VOWELS = {"a", "i", "u", "e", "o"}


class ContextResolver:
    """Resolves ``pending_sokuon``/``pending_syllabic_n`` against the next
    token's romanized text.

    Operates on a Token-aligned sequence: one slot per Token, where a
    ``None`` slot means that token had no kana romanization at all (e.g.
    punctuation) and is both passed through unchanged and treated as "no
    phonetic content to resolve against" for the *previous* token's pending
    state, same as running off the end of the sequence.
    """

    def resolve(
        self, romanizations: Sequence[KanaRomanization | None]
    ) -> tuple[KanaRomanization | None, ...]:
        n = len(romanizations)
        resolved: list[KanaRomanization | None] = list(romanizations)

        for i, kr in enumerate(romanizations):
            if kr is None or not (kr.pending_sokuon or kr.pending_syllabic_n):
                continue

            next_kr = romanizations[i + 1] if i + 1 < n else None
            resolved[i] = _resolve_one(kr, next_kr)

        return tuple(resolved)


def _resolve_one(
    kr: KanaRomanization, next_kr: KanaRomanization | None
) -> KanaRomanization:
    next_text = next_kr.text if next_kr is not None else ""
    text = kr.text
    pending_sokuon = kr.pending_sokuon
    pending_syllabic_n = kr.pending_syllabic_n

    if pending_sokuon:
        text += sokuon_prefix(next_text) if next_text else "'"
        pending_sokuon = False

    if pending_syllabic_n:
        if next_text and (next_text[0] in _VOWELS or next_text.startswith("y")):
            text += "'"
        pending_syllabic_n = False

    return replace(
        kr,
        text=text,
        pending_sokuon=pending_sokuon,
        pending_syllabic_n=pending_syllabic_n,
    )
