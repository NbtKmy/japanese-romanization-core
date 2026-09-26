"""Kana input normalization for KanaRomanizer (kana_romanizer_spec.md §6).

``prepare_kana`` never mutates its input; it returns a new, normalized
string built from three steps: Unicode NFC normalization, half-width
katakana -> full-width katakana, and katakana -> hiragana. Full-text NFKC
normalization is deliberately not used anywhere in this module.
"""

import unicodedata

_HALFWIDTH_TO_FULLWIDTH: dict[str, str] = {
    "ｦ": "ヲ",
    "ｧ": "ァ",
    "ｨ": "ィ",
    "ｩ": "ゥ",
    "ｪ": "ェ",
    "ｫ": "ォ",
    "ｬ": "ャ",
    "ｭ": "ュ",
    "ｮ": "ョ",
    "ｯ": "ッ",
    "ｰ": "ー",
    "ｱ": "ア",
    "ｲ": "イ",
    "ｳ": "ウ",
    "ｴ": "エ",
    "ｵ": "オ",
    "ｶ": "カ",
    "ｷ": "キ",
    "ｸ": "ク",
    "ｹ": "ケ",
    "ｺ": "コ",
    "ｻ": "サ",
    "ｼ": "シ",
    "ｽ": "ス",
    "ｾ": "セ",
    "ｿ": "ソ",
    "ﾀ": "タ",
    "ﾁ": "チ",
    "ﾂ": "ツ",
    "ﾃ": "テ",
    "ﾄ": "ト",
    "ﾅ": "ナ",
    "ﾆ": "ニ",
    "ﾇ": "ヌ",
    "ﾈ": "ネ",
    "ﾉ": "ノ",
    "ﾊ": "ハ",
    "ﾋ": "ヒ",
    "ﾌ": "フ",
    "ﾍ": "ヘ",
    "ﾎ": "ホ",
    "ﾏ": "マ",
    "ﾐ": "ミ",
    "ﾑ": "ム",
    "ﾒ": "メ",
    "ﾓ": "モ",
    "ﾔ": "ヤ",
    "ﾕ": "ユ",
    "ﾖ": "ヨ",
    "ﾗ": "ラ",
    "ﾘ": "リ",
    "ﾙ": "ル",
    "ﾚ": "レ",
    "ﾛ": "ロ",
    "ﾜ": "ワ",
    "ﾝ": "ン",
}

_DAKUTEN_COMBOS: dict[str, str] = {
    "カ": "ガ",
    "キ": "ギ",
    "ク": "グ",
    "ケ": "ゲ",
    "コ": "ゴ",
    "サ": "ザ",
    "シ": "ジ",
    "ス": "ズ",
    "セ": "ゼ",
    "ソ": "ゾ",
    "タ": "ダ",
    "チ": "ヂ",
    "ツ": "ヅ",
    "テ": "デ",
    "ト": "ド",
    "ハ": "バ",
    "ヒ": "ビ",
    "フ": "ブ",
    "ヘ": "ベ",
    "ホ": "ボ",
    "ウ": "ヴ",
}

_HANDAKUTEN_COMBOS: dict[str, str] = {
    "ハ": "パ",
    "ヒ": "ピ",
    "フ": "プ",
    "ヘ": "ペ",
    "ホ": "ポ",
}

_HALFWIDTH_DAKUTEN = "ﾞ"
_HALFWIDTH_HANDAKUTEN = "ﾟ"

_KATAKANA_RANGE_START = ord("ァ")
_KATAKANA_RANGE_END = ord("ヶ")
_KATAKANA_TO_HIRAGANA_OFFSET = ord("ア") - ord("あ")


def _halfwidth_katakana_to_fullwidth(text: str) -> str:
    out: list[str] = []
    i = 0
    n = len(text)

    while i < n:
        char = text[i]
        base = _HALFWIDTH_TO_FULLWIDTH.get(char)

        if base is None:
            out.append(char)
            i += 1
            continue

        if i + 1 < n:
            next_char = text[i + 1]
            if next_char == _HALFWIDTH_DAKUTEN and base in _DAKUTEN_COMBOS:
                out.append(_DAKUTEN_COMBOS[base])
                i += 2
                continue
            if next_char == _HALFWIDTH_HANDAKUTEN and base in _HANDAKUTEN_COMBOS:
                out.append(_HANDAKUTEN_COMBOS[base])
                i += 2
                continue

        out.append(base)
        i += 1

    return "".join(out)


def _katakana_to_hiragana(text: str) -> str:
    out: list[str] = []

    for char in text:
        codepoint = ord(char)
        if _KATAKANA_RANGE_START <= codepoint <= _KATAKANA_RANGE_END:
            out.append(chr(codepoint - _KATAKANA_TO_HIRAGANA_OFFSET))
        else:
            out.append(char)

    return "".join(out)


def prepare_kana(kana: str) -> str:
    normalized = unicodedata.normalize("NFC", kana)
    widened = _halfwidth_katakana_to_fullwidth(normalized)
    return _katakana_to_hiragana(widened)
