"""Exception hierarchy for romanizer_core.

All exceptions raised by this package's public API derive from
``RomanizerCoreError``, so callers can catch that single type to handle
any failure originating in romanizer_core. Leaf exceptions below indicate
more specific causes: configuration/setup problems (dictionary path
issues, mismatched schemas), MeCab initialization failures, errors
encountered while analyzing text (span resolution, UniDic feature
parsing), and kana romanization scheme errors (duplicate mapping keys,
unknown scheme lookups).
"""

from pathlib import Path


class RomanizerCoreError(Exception):
    """Root of the romanizer_core exception hierarchy; catch this to handle any package error."""


class AnalyzerError(RomanizerCoreError):
    """Base class for errors raised by the analyzer layer (configuration, dictionary, or analysis failures)."""


class AnalyzerConfigurationError(AnalyzerError):
    """Raised when an analyzer is misconfigured, e.g. a supplied parser's schema does not match the dictionary's schema."""


class DictionaryError(AnalyzerError):
    """Base class for errors about the configured dictionary path."""


class DictionaryNotFoundError(DictionaryError):
    """Raised when the configured dictionary path does not exist."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Dictionary not found: {path}")


class InvalidDictionaryError(DictionaryError):
    """Raised when the configured dictionary path exists but is not a directory."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Invalid dictionary directory: {path}")


class MeCabInitializationError(AnalyzerError):
    """Raised when the underlying MeCab tagger fails to initialize (e.g. an unusable dictionary)."""


class AnalysisError(AnalyzerError):
    """Raised when analyzing text fails, including invalid input (e.g. embedded NUL characters) or unexpected MeCab errors."""


class SpanResolutionError(AnalysisError):
    """Raised when a token's surface form cannot be located in the original text from the current cursor position."""

    def __init__(self, *, surface: str, cursor: int) -> None:
        self.surface = surface
        self.cursor = cursor
        super().__init__(
            f"Could not find surface {surface!r} in text starting at index {cursor}"
        )


class UniDicError(AnalyzerError):
    """Base class for errors parsing UniDic node features."""


class UniDicFeatureParseError(UniDicError):
    """Raised when a raw MeCab node feature string cannot be parsed as CSV."""

    def __init__(self, raw_feature: str) -> None:
        self.raw_feature = raw_feature
        super().__init__(f"Failed to parse UniDic feature as CSV: {raw_feature!r}")


class UnsupportedUniDicSchemaError(UniDicError):
    """Raised when a known-node feature's field count doesn't match the configured schema, or the schema id is unrecognized."""

    def __init__(
        self,
        schema_id: str,
        *,
        expected: int | None = None,
        actual: int | None = None,
        surface: str | None = None,
        feature: str | None = None,
    ) -> None:
        self.schema_id = schema_id
        self.expected = expected
        self.actual = actual
        self.surface = surface
        self.feature = feature
        if expected is not None and actual is not None:
            message = (
                f"Schema {schema_id!r} expects {expected} known-node fields, "
                f"got {actual} for surface {surface!r} (feature={feature!r})"
            )
        else:
            message = f"Unknown UniDic schema id: {schema_id!r}"
        super().__init__(message)


class InvalidUnknownFeatureError(UniDicError):
    """Raised when an unknown-node feature has fewer fields than the schema's unknown-node field set requires."""

    def __init__(
        self,
        *,
        expected_at_least: int,
        actual: int,
        surface: str,
        feature: str,
    ) -> None:
        self.expected_at_least = expected_at_least
        self.actual = actual
        self.surface = surface
        self.feature = feature
        super().__init__(
            "Unknown-node feature too short: expected at least "
            f"{expected_at_least} fields, got {actual} for surface {surface!r} "
            f"(feature={feature!r})"
        )


class KanaError(RomanizerCoreError):
    """Base class for errors raised by the kana romanization layer."""


class DuplicateKanaMappingError(KanaError):
    """Raised when the same kana key appears in more than one mapping table of a KanaSchemeDefinition."""

    def __init__(self, key: str, *, sources: tuple[str, str]) -> None:
        self.key = key
        self.sources = sources
        super().__init__(
            f"Kana key {key!r} is defined in multiple mapping tables: "
            f"{sources[0]!r} and {sources[1]!r}"
        )


class UnknownKanaSchemeError(KanaError):
    """Raised when get_scheme() is called with an unregistered (name, version) pair."""

    def __init__(self, name: str, version: str) -> None:
        self.name = name
        self.version = version
        super().__init__(f"Unknown kana scheme: name={name!r}, version={version!r}")
