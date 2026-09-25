from dataclasses import dataclass

from .token import Token


@dataclass(frozen=True, slots=True)
class DictionaryInfo:
    name: str
    version: str | None
    schema_id: str


@dataclass(frozen=True, slots=True)
class AnalyzerInfo:
    name: str
    version: str | None
    dictionary: DictionaryInfo


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    text: str
    analyzer: AnalyzerInfo
    tokens: tuple[Token, ...]
