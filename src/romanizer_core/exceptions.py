from pathlib import Path


class RomanizerCoreError(Exception):
    pass


class AnalyzerError(RomanizerCoreError):
    pass


class AnalyzerConfigurationError(AnalyzerError):
    pass


class DictionaryError(AnalyzerError):
    pass


class DictionaryNotFoundError(DictionaryError):
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Dictionary not found: {path}")


class InvalidDictionaryError(DictionaryError):
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Invalid dictionary directory: {path}")


class MeCabInitializationError(AnalyzerError):
    pass


class AnalysisError(AnalyzerError):
    pass


class SpanResolutionError(AnalysisError):
    def __init__(self, *, surface: str, cursor: int) -> None:
        self.surface = surface
        self.cursor = cursor
        super().__init__(
            f"Could not find surface {surface!r} in text starting at index {cursor}"
        )


class UniDicError(AnalyzerError):
    pass


class UniDicFeatureParseError(UniDicError):
    def __init__(self, raw_feature: str) -> None:
        self.raw_feature = raw_feature
        super().__init__(f"Failed to parse UniDic feature as CSV: {raw_feature!r}")


class UnsupportedUniDicSchemaError(UniDicError):
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
