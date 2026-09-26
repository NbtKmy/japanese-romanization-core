import pytest

from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("きゃ", "kya"),
        ("しゃ", "sha"),
        ("ちゃ", "cha"),
        ("じゃ", "ja"),
        ("ぢゃ", "ja"),
        ("にゃ", "nya"),
        ("ひゃ", "hya"),
        ("みゃ", "mya"),
        ("りゃ", "rya"),
        ("ぎゃ", "gya"),
        ("びゃ", "bya"),
        ("ぴゃ", "pya"),
    ],
)
def test_standard_yoon(kana, expected):
    assert romanizer.romanize(kana).text == expected


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("ゃ", "ya"),
        ("ゅ", "yu"),
        ("ょ", "yo"),
        ("ぁ", "a"),
        ("ぃ", "i"),
        ("ぅ", "u"),
        ("ぇ", "e"),
        ("ぉ", "o"),
    ],
)
def test_isolated_small_kana_fallback_does_not_crash(kana, expected):
    assert romanizer.romanize(kana).text == expected
