from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DictionaryConfig:
    path: Path
    name: str = "unidic-cwj"
    version: str | None = None
    schema_id: str = "unidic-cwj-202512-29"


@dataclass(frozen=True, slots=True)
class MeCabAnalyzerConfig:
    dictionary: DictionaryConfig
    validate_dictionary: bool = True
