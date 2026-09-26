from dataclasses import dataclass

from .token import Token


@dataclass(frozen=True, slots=True)
class DictionaryInfo:
    """Identifying info about the dictionary an analyzer was built with; deliberately never includes the dictionary's filesystem path."""

    name: str
    version: str | None
    schema_id: str


@dataclass(frozen=True, slots=True)
class AnalyzerInfo:
    """Identifying info about an analyzer (name, version) and the dictionary it uses."""

    name: str
    version: str | None
    dictionary: DictionaryInfo


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """The full, immutable result of analyzing one piece of text."""

    text: str
    analyzer: AnalyzerInfo
    tokens: tuple[Token, ...]
