import csv
from dataclasses import dataclass
from io import StringIO

from ..exceptions import UniDicFeatureParseError, UnsupportedUniDicSchemaError
from ..models.token import Token
from .schema import UniDicSchema


@dataclass(frozen=True, slots=True)
class RawToken:
    id: str
    surface: str
    start: int
    end: int
    is_unknown: bool
    feature: str


def _parse_csv_feature(raw: str) -> list[str]:
    try:
        return next(csv.reader(StringIO(raw)))
    except (csv.Error, StopIteration) as exc:
        raise UniDicFeatureParseError(raw) from exc


def _optional(value: str | None) -> str | None:
    if value is None or value in ("", "*"):
        return None
    return value


def _normalize_pos(*values: str | None) -> tuple[str, ...]:
    return tuple(value for value in values if value not in (None, "", "*"))


class UniDicParser:
    def __init__(self, schema: UniDicSchema) -> None:
        self._schema = schema

    @property
    def schema(self) -> UniDicSchema:
        return self._schema

    def parse_known(self, raw: RawToken) -> Token:
        fields = _parse_csv_feature(raw.feature)
        expected = self._schema.known_fields

        if len(fields) != len(expected):
            raise UnsupportedUniDicSchemaError(
                self._schema.id,
                expected=len(expected),
                actual=len(fields),
                surface=raw.surface,
                feature=raw.feature,
            )

        values = dict(zip(expected, fields, strict=True))

        return Token(
            id=raw.id,
            surface=raw.surface,
            start=raw.start,
            end=raw.end,
            is_unknown=False,
            lemma=_optional(values["lemma"]),
            lemma_reading=_optional(values["lForm"]),
            pos=_normalize_pos(
                values["pos1"], values["pos2"], values["pos3"], values["pos4"],
            ),
            conjugation_type=_optional(values["cType"]),
            conjugation_form=_optional(values["cForm"]),
            orth=_optional(values["orth"]),
            kana=_optional(values["kana"]),
            pronunciation=_optional(values["pron"]),
            form=_optional(values["form"]),
            form_base=_optional(values["formBase"]),
            word_type=_optional(values["goshu"]),
        )
