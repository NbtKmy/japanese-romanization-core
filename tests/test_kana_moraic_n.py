import pytest

from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("しんぶん", "shinbun"),
        ("かんぱい", "kanpai"),
        ("しんいち", "shin'ichi"),
        ("きんようび", "kin'yōbi"),
    ],
)
def test_moraic_n(kana, expected):
    assert romanizer.romanize(kana).text == expected


def test_moraic_n_at_end_of_string_sets_pending_flag_and_stays_n():
    result = romanizer.romanize("かん")
    assert result.pending_syllabic_n is True
    assert result.text == "kan"


def test_isolated_moraic_n_does_not_crash():
    result = romanizer.romanize("ん")
    assert result.pending_syllabic_n is True
    assert result.text == "n"


def test_moraic_n_before_unmappable_text_is_not_pending():
    result = romanizer.romanize("ん5")
    assert result.pending_syllabic_n is False
    assert result.text == "n5"
