import pytest

from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("べんきょう", "benkyō"),  # yōon + moraic n + ou->ō contraction
        ("みっつ", "mittsu"),  # sokuon prefix
        ("びょういん", "byōin"),  # yōon + ou->ō + retained "ei"-shaped い + token-final ん
    ],
)
def test_multi_rule_regression(kana, expected):
    assert romanizer.romanize(kana).text == expected


def test_token_final_moraic_n_after_multi_rule_word_reports_pending():
    result = romanizer.romanize("びょういん")
    assert result.text == "byōin"
    assert result.pending_syllabic_n is True
