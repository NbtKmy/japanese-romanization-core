"""Rare extended-katakana combinations (kana_romanizer_spec.md Part III, §25).

Spec §25 gives ``sw``, ``tw``, ``dw``, ``fw``, ``rw`` as examples without
mandating a complete table; entries may be added incrementally. ``fw`` is
intentionally omitted here: the kana it would need (``ふぁ``) is already
claimed by MODERN_KANA_EXTENSIONS's ``fa`` entry, and there is no
well-established distinct kana spelling for the ``fwa``-style sound in this
project's small-kana-after-consonant convention, so adding it would mean
guessing a spelling rather than encoding an established one.
"""

RARE_KANA_EXTENSIONS: dict[str, str] = {
    "すぁ": "swa",
    "すぃ": "swi",
    "すぇ": "swe",
    "すぉ": "swo",
    "とぁ": "twa",
    "とぃ": "twi",
    "とぇ": "twe",
    "とぉ": "two",
    "どぁ": "dwa",
    "どぃ": "dwi",
    "どぇ": "dwe",
    "どぉ": "dwo",
    "るぁ": "rwa",
    "るぃ": "rwi",
    "るぇ": "rwe",
    "るぉ": "rwo",
}
