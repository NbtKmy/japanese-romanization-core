import pytest

from romanizer_core.kana.mapping_base import BASE_KANA_MAPPING


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("あ", "a"),
        ("い", "i"),
        ("う", "u"),
        ("え", "e"),
        ("お", "o"),
        ("し", "shi"),
        ("ち", "chi"),
        ("つ", "tsu"),
        ("ふ", "fu"),
        ("じ", "ji"),
        ("ぢ", "ji"),
        ("づ", "zu"),
        ("を", "wo"),
        ("は", "ha"),
        ("へ", "he"),
    ],
)
def test_modified_hepburn_base(kana, expected):
    assert BASE_KANA_MAPPING[kana] == expected


def test_special_characters_are_not_mapping_keys():
    assert "っ" not in BASE_KANA_MAPPING
    assert "ん" not in BASE_KANA_MAPPING
    assert "ー" not in BASE_KANA_MAPPING


def test_all_values_are_ascii_romaji():
    for romaji in BASE_KANA_MAPPING.values():
        assert romaji.isascii()
