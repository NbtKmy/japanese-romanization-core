"""Base gojūon (plain, voiced, semi-voiced) hiragana-to-romaji mapping.

Yōon (contracted-sound) and isolated small-kana fallback entries are added
separately once the longest-match scanner exists; see mapping_base.py's
sibling additions in later implementation steps.

``っ``, ``ん``, and ``ー`` are deliberately absent from this table: the
KanaRomanizer scanner branches on them before consulting any mapping table,
and their presence here would make that branching ambiguous.
"""

BASE_KANA_MAPPING: dict[str, str] = {
    # Vowels
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    # K row
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    # S row
    "さ": "sa",
    "し": "shi",
    "す": "su",
    "せ": "se",
    "そ": "so",
    # T row
    "た": "ta",
    "ち": "chi",
    "つ": "tsu",
    "て": "te",
    "と": "to",
    # N row
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    # H row
    "は": "ha",
    "ひ": "hi",
    "ふ": "fu",
    "へ": "he",
    "ほ": "ho",
    # M row
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    # Y row
    "や": "ya",
    "ゆ": "yu",
    "よ": "yo",
    # R row
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    # W row
    "わ": "wa",
    "を": "wo",
    # G row
    "が": "ga",
    "ぎ": "gi",
    "ぐ": "gu",
    "げ": "ge",
    "ご": "go",
    # Z row
    "ざ": "za",
    "じ": "ji",
    "ず": "zu",
    "ぜ": "ze",
    "ぞ": "zo",
    # D row
    "だ": "da",
    "ぢ": "ji",
    "づ": "zu",
    "で": "de",
    "ど": "do",
    # B row
    "ば": "ba",
    "び": "bi",
    "ぶ": "bu",
    "べ": "be",
    "ぼ": "bo",
    # P row
    "ぱ": "pa",
    "ぴ": "pi",
    "ぷ": "pu",
    "ぺ": "pe",
    "ぽ": "po",
    # Standard yōon (spec §28) — explicit entries, not derived mechanically
    # from consonant stripping, because し/ち already have Hepburn-specific
    # consonant shapes (shi/chi) that carry over irregularly into sha/cha.
    "きゃ": "kya",
    "きゅ": "kyu",
    "きょ": "kyo",
    "しゃ": "sha",
    "しゅ": "shu",
    "しょ": "sho",
    "ちゃ": "cha",
    "ちゅ": "chu",
    "ちょ": "cho",
    "にゃ": "nya",
    "にゅ": "nyu",
    "にょ": "nyo",
    "ひゃ": "hya",
    "ひゅ": "hyu",
    "ひょ": "hyo",
    "みゃ": "mya",
    "みゅ": "myu",
    "みょ": "myo",
    "りゃ": "rya",
    "りゅ": "ryu",
    "りょ": "ryo",
    "ぎゃ": "gya",
    "ぎゅ": "gyu",
    "ぎょ": "gyo",
    "じゃ": "ja",
    "じゅ": "ju",
    "じょ": "jo",
    "びゃ": "bya",
    "びゅ": "byu",
    "びょ": "byo",
    "ぴゃ": "pya",
    "ぴゅ": "pyu",
    "ぴょ": "pyo",
    "ぢゃ": "ja",
    "ぢゅ": "ju",
    "ぢょ": "jo",
    # Isolated small kana fallback (spec §29): only used when no combined
    # mapping consumed them as part of a yōon/extension digraph above.
    "ゃ": "ya",
    "ゅ": "yu",
    "ょ": "yo",
    "ぁ": "a",
    "ぃ": "i",
    "ぅ": "u",
    "ぇ": "e",
    "ぉ": "o",
}
