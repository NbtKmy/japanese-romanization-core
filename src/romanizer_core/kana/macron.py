"""Vowel-to-macron table for chōonpu and default long-vowel contraction (kana_romanizer_spec.md §40).

Kept separate from mapping_base.py so a future LongVowelResolver can import
just this table without pulling in the full gojūon mapping.
"""

MACRON: dict[str, str] = {
    "a": "ā",
    "i": "ī",
    "u": "ū",
    "e": "ē",
    "o": "ō",
}

MACRON_TO_VOWEL: dict[str, str] = {macron: vowel for vowel, macron in MACRON.items()}
