from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from ..exceptions import DuplicateKanaMappingError, UnknownKanaSchemeError
from .mapping_base import BASE_KANA_MAPPING
from .mapping_modern import MODERN_KANA_EXTENSIONS
from .mapping_rare import RARE_KANA_EXTENSIONS


@dataclass(frozen=True, slots=True)
class KanaSchemeDefinition:
    """A named, versioned kana-to-romaji mapping profile.

    ``base_mapping``, ``modern_extensions``, and ``rare_extensions`` must not
    share any keys; ``__post_init__`` enforces this and replaces each field
    with an immutable ``MappingProxyType`` view over its own dict copy.
    """

    name: str
    version: str
    base_mapping: Mapping[str, str]
    modern_extensions: Mapping[str, str]
    rare_extensions: Mapping[str, str]

    def __post_init__(self) -> None:
        tables = {
            "base_mapping": dict(self.base_mapping),
            "modern_extensions": dict(self.modern_extensions),
            "rare_extensions": dict(self.rare_extensions),
        }

        seen: dict[str, str] = {}
        for source_name, table in tables.items():
            for key in table:
                if key in seen:
                    raise DuplicateKanaMappingError(
                        key, sources=(seen[key], source_name)
                    )
                seen[key] = source_name

        for source_name, table in tables.items():
            object.__setattr__(self, source_name, MappingProxyType(table))


MODIFIED_HEPBURN_V1 = KanaSchemeDefinition(
    name="modified_hepburn",
    version="1",
    base_mapping=BASE_KANA_MAPPING,
    modern_extensions=MODERN_KANA_EXTENSIONS,
    rare_extensions=RARE_KANA_EXTENSIONS,
)

SCHEMES: dict[tuple[str, str], KanaSchemeDefinition] = {
    (MODIFIED_HEPBURN_V1.name, MODIFIED_HEPBURN_V1.version): MODIFIED_HEPBURN_V1,
}


def get_scheme(name: str, version: str) -> KanaSchemeDefinition:
    try:
        return SCHEMES[(name, version)]
    except KeyError as exc:
        raise UnknownKanaSchemeError(name, version) from exc
