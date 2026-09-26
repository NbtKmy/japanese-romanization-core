import pytest
from types import MappingProxyType

from romanizer_core.exceptions import DuplicateKanaMappingError, UnknownKanaSchemeError
from romanizer_core.kana.scheme import KanaSchemeDefinition, SCHEMES, get_scheme


def test_valid_scheme_combines_without_error():
    definition = KanaSchemeDefinition(
        name="test",
        version="1",
        base_mapping={"あ": "a"},
        modern_extensions={"ゔ": "vu"},
        rare_extensions={"ぐぁ": "gwa"},
    )
    assert definition.base_mapping["あ"] == "a"
    assert definition.modern_extensions["ゔ"] == "vu"
    assert definition.rare_extensions["ぐぁ"] == "gwa"


def test_scheme_tables_are_immutable_mapping_proxies():
    definition = KanaSchemeDefinition(
        name="test",
        version="1",
        base_mapping={"あ": "a"},
        modern_extensions={},
        rare_extensions={},
    )
    assert isinstance(definition.base_mapping, MappingProxyType)
    with pytest.raises(TypeError):
        definition.base_mapping["い"] = "i"  # type: ignore[index]


def test_duplicate_key_across_base_and_modern_raises():
    with pytest.raises(DuplicateKanaMappingError) as exc_info:
        KanaSchemeDefinition(
            name="test",
            version="1",
            base_mapping={"あ": "a"},
            modern_extensions={"あ": "a"},
            rare_extensions={},
        )
    assert exc_info.value.key == "あ"
    assert exc_info.value.sources == ("base_mapping", "modern_extensions")


def test_duplicate_key_across_modern_and_rare_raises():
    with pytest.raises(DuplicateKanaMappingError):
        KanaSchemeDefinition(
            name="test",
            version="1",
            base_mapping={},
            modern_extensions={"ゔぁ": "va"},
            rare_extensions={"ゔぁ": "va"},
        )


def test_get_scheme_raises_for_unknown_name_version():
    with pytest.raises(UnknownKanaSchemeError) as exc_info:
        get_scheme("does-not-exist", "1")
    assert exc_info.value.name == "does-not-exist"
    assert exc_info.value.version == "1"


def test_get_scheme_returns_registered_scheme():
    definition = KanaSchemeDefinition(
        name="registry-test",
        version="1",
        base_mapping={},
        modern_extensions={},
        rare_extensions={},
    )
    SCHEMES[(definition.name, definition.version)] = definition
    try:
        assert get_scheme("registry-test", "1") is definition
    finally:
        del SCHEMES[(definition.name, definition.version)]
