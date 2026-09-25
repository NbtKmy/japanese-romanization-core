from dataclasses import dataclass

from ..exceptions import UnsupportedUniDicSchemaError


@dataclass(frozen=True, slots=True)
class UniDicSchema:
    id: str
    known_fields: tuple[str, ...]
    unknown_fields: tuple[str, ...]


UNIDIC_CWJ_202512_SCHEMA = UniDicSchema(
    id="unidic-cwj-202512-29",
    known_fields=(
        "pos1",
        "pos2",
        "pos3",
        "pos4",
        "cType",
        "cForm",
        "lForm",
        "lemma",
        "orth",
        "pron",
        "orthBase",
        "pronBase",
        "goshu",
        "iType",
        "iForm",
        "fType",
        "fForm",
        "iConType",
        "fConType",
        "type",
        "kana",
        "kanaBase",
        "form",
        "formBase",
        "aType",
        "aConType",
        "aModType",
        "lid",
        "lemma_id",
    ),
    unknown_fields=("pos1", "pos2", "pos3", "pos4", "cType", "cForm"),
)

SCHEMAS: dict[str, UniDicSchema] = {
    UNIDIC_CWJ_202512_SCHEMA.id: UNIDIC_CWJ_202512_SCHEMA,
}


def get_schema(schema_id: str) -> UniDicSchema:
    try:
        return SCHEMAS[schema_id]
    except KeyError as exc:
        raise UnsupportedUniDicSchemaError(schema_id) from exc
