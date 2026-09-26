"""Kana iteration mark resolution (kana_romanizer_spec.md §45).

``ゝ``/``ヽ`` repeat the preceding mora as-is; ``ゞ``/``ヾ`` repeat it with
dakuten where a voiced counterpart exists. Invalid usage (no preceding
mora, or no voiced counterpart) must not raise — callers fall back to
preserving the mark verbatim.
"""

from typing import Mapping

from .scanner import longest_match

_VOICED_COMBOS: dict[str, str] = {
    "か": "が",
    "き": "ぎ",
    "く": "ぐ",
    "け": "げ",
    "こ": "ご",
    "さ": "ざ",
    "し": "じ",
    "す": "ず",
    "せ": "ぜ",
    "そ": "ぞ",
    "た": "だ",
    "ち": "ぢ",
    "つ": "づ",
    "て": "で",
    "と": "ど",
    "は": "ば",
    "ひ": "び",
    "ふ": "ぶ",
    "へ": "べ",
    "ほ": "ぼ",
}


def resolve_iteration_mark(
    *, mark: str, last_mora_kana: str | None, lookup: Mapping[str, str]
) -> tuple[str, str] | None:
    """Resolve a kana iteration mark against the preceding mora.

    Returns ``(mora_kana, romaji)`` for the repeated mora, or ``None`` if
    it cannot be resolved (no preceding mora, or a voiced-repeat of a mora
    that has no voiced counterpart).
    """

    if last_mora_kana is None:
        return None

    if mark in ("ゞ", "ヾ"):
        repeated_kana = _VOICED_COMBOS.get(last_mora_kana)
        if repeated_kana is None:
            return None
    else:
        repeated_kana = last_mora_kana

    match = longest_match(repeated_kana, 0, lookup)
    if match is None or match[0] != repeated_kana:
        return None

    _, romaji = match
    return repeated_kana, romaji
