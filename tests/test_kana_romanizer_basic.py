import pytest

from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("し", "shi"),
        ("ち", "chi"),
        ("つ", "tsu"),
        ("ふ", "fu"),
        ("じ", "ji"),
        ("ぢ", "ji"),
        ("づ", "zu"),
        ("あい", "ai"),
        ("かき", "kaki"),
    ],
)
def test_basic_conversion(kana, expected):
    assert romanizer.romanize(kana).text == expected


def test_empty_string_returns_empty_text():
    result = romanizer.romanize("")
    assert result.text == ""
    assert result.pending_sokuon is False
    assert result.pending_syllabic_n is False
    assert result.final_vowel is None


def test_mixed_ascii_passes_through_unmapped_characters():
    assert romanizer.romanize("かなA1").text == "kanaA1"


def test_non_str_input_raises_type_error():
    with pytest.raises(TypeError):
        romanizer.romanize(123)  # type: ignore[arg-type]


def test_final_vowel_reflects_trailing_mora():
    result = romanizer.romanize("かき")
    assert result.final_vowel == "i"
