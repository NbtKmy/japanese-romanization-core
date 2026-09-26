import pytest

from romanizer_core.kana.mapping_rare import RARE_KANA_EXTENSIONS


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("すぁ", "swa"),
        ("とぁ", "twa"),
        ("どぁ", "dwa"),
        ("るぁ", "rwa"),
    ],
)
def test_rare_kana_extensions(kana, expected):
    assert RARE_KANA_EXTENSIONS[kana] == expected


def test_fw_is_intentionally_absent():
    assert "ふぁ" not in RARE_KANA_EXTENSIONS
