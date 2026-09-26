import pytest

from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("いっしょ", "issho"),
        ("まっちゃ", "matcha"),
        ("いっち", "itchi"),
        ("がっこう", "gakkō"),
        ("いっつう", "ittsū"),
    ],
)
def test_sokuon_prefix(kana, expected):
    assert romanizer.romanize(kana).text == expected


def test_sokuon_at_end_of_string_sets_pending_flag():
    result = romanizer.romanize("あっ")
    assert result.pending_sokuon is True
    assert result.text == "a"


def test_isolated_sokuon_does_not_crash():
    result = romanizer.romanize("っ")
    assert result.pending_sokuon is True
    assert result.text == ""


def test_sokuon_followed_by_unmappable_text_defers_rather_than_guesses():
    result = romanizer.romanize("あっ5")
    assert result.pending_sokuon is True
    assert result.text == "a5"
