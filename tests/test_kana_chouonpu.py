import pytest

from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("セーラー", "sērā"),
        ("パーティー", "pātī"),
        ("タクシー", "takushī"),
        ("スーパー", "sūpā"),
    ],
)
def test_chouonpu_lengthens_preceding_vowel(kana, expected):
    assert romanizer.romanize(kana).text == expected


def test_chouonpu_at_start_of_string_is_preserved():
    result = romanizer.romanize("ー")
    assert result.text == "ー"


def test_chouonpu_after_non_vowel_ending_mora_is_preserved():
    # ん never leaves a plain vowel behind, so a following ー has nothing
    # to lengthen and must not crash.
    result = romanizer.romanize("かんー")
    assert result.text == "kanー"
