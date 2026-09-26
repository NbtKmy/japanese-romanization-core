import pytest

from romanizer_core.kana.mapping_modern import MODERN_KANA_EXTENSIONS


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("ふぁ", "fa"),
        ("ふぃ", "fi"),
        ("ふぇ", "fe"),
        ("ふぉ", "fo"),
        ("てぃ", "ti"),
        ("とぅ", "tu"),
        ("でぃ", "di"),
        ("どぅ", "du"),
        ("しぇ", "she"),
        ("じぇ", "je"),
        ("ちぇ", "che"),
        ("つぁ", "tsa"),
        ("つぃ", "tsi"),
        ("つぇ", "tse"),
        ("つぉ", "tso"),
        ("ゔぁ", "va"),
        ("ゔぃ", "vi"),
        ("ゔ", "vu"),
        ("ゔぇ", "ve"),
        ("ゔぉ", "vo"),
    ],
)
def test_modern_kana_extensions(kana, expected):
    assert MODERN_KANA_EXTENSIONS[kana] == expected
