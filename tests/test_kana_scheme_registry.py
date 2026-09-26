import pytest

from romanizer_core.exceptions import UnknownKanaSchemeError
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1, get_scheme


def test_get_scheme_returns_modified_hepburn_v1():
    scheme = get_scheme("modified_hepburn", "1")
    assert scheme is MODIFIED_HEPBURN_V1


def test_modified_hepburn_v1_combines_all_tables():
    assert MODIFIED_HEPBURN_V1.base_mapping["あ"] == "a"
    assert MODIFIED_HEPBURN_V1.modern_extensions["ふぁ"] == "fa"
    assert MODIFIED_HEPBURN_V1.rare_extensions["すぁ"] == "swa"


def test_get_scheme_raises_for_unknown_version():
    with pytest.raises(UnknownKanaSchemeError):
        get_scheme("modified_hepburn", "999")
