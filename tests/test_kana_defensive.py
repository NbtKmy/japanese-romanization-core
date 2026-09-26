import pytest

from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


@pytest.mark.parametrize(
    "kana",
    [
        "っ",
        "ー",
        "ゃ",
        "ゞ",
        "々",
        "ヷ",  # rare combined katakana absent from every mapping table
        "かなABC123",
    ],
)
def test_defensive_inputs_do_not_raise(kana):
    romanizer.romanize(kana)


def test_output_is_deterministic():
    kana = "がっこうへいきますとうきょうしんぶんをよみながら"
    first = romanizer.romanize(kana)
    second = romanizer.romanize(kana)
    assert first == second
