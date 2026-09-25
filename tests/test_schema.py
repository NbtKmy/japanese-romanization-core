import pytest

from romanizer_core.analyzer.schema import UNIDIC_CWJ_202512_SCHEMA, get_schema
from romanizer_core.exceptions import UnsupportedUniDicSchemaError


def test_unidic_cwj_202512_schema_has_29_known_fields():
    assert len(UNIDIC_CWJ_202512_SCHEMA.known_fields) == 29
    assert UNIDIC_CWJ_202512_SCHEMA.known_fields[0] == "pos1"
    assert UNIDIC_CWJ_202512_SCHEMA.known_fields[8] == "orth"
    assert UNIDIC_CWJ_202512_SCHEMA.known_fields[9] == "pron"
    assert UNIDIC_CWJ_202512_SCHEMA.known_fields[10] == "orthBase"
    assert UNIDIC_CWJ_202512_SCHEMA.known_fields[11] == "pronBase"
    assert UNIDIC_CWJ_202512_SCHEMA.known_fields[-2] == "lid"
    assert UNIDIC_CWJ_202512_SCHEMA.known_fields[-1] == "lemma_id"


def test_unidic_cwj_202512_schema_has_6_unknown_fields():
    assert UNIDIC_CWJ_202512_SCHEMA.unknown_fields == (
        "pos1",
        "pos2",
        "pos3",
        "pos4",
        "cType",
        "cForm",
    )


def test_get_schema_returns_registered_schema():
    schema = get_schema("unidic-cwj-202512-29")
    assert schema is UNIDIC_CWJ_202512_SCHEMA


def test_get_schema_raises_for_unknown_id():
    with pytest.raises(UnsupportedUniDicSchemaError) as exc_info:
        get_schema("does-not-exist")
    assert exc_info.value.schema_id == "does-not-exist"
