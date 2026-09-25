from pathlib import Path

import pytest

from romanizer_core.exceptions import (
    AnalysisError,
    AnalyzerConfigurationError,
    AnalyzerError,
    DictionaryError,
    DictionaryNotFoundError,
    InvalidDictionaryError,
    InvalidUnknownFeatureError,
    MeCabInitializationError,
    RomanizerCoreError,
    SpanResolutionError,
    UniDicError,
    UniDicFeatureParseError,
    UnsupportedUniDicSchemaError,
)


def test_hierarchy_roots_at_romanizer_core_error():
    for exc_type in (
        AnalyzerError,
        AnalyzerConfigurationError,
        DictionaryError,
        DictionaryNotFoundError,
        InvalidDictionaryError,
        MeCabInitializationError,
        AnalysisError,
        SpanResolutionError,
        UniDicError,
        UniDicFeatureParseError,
        UnsupportedUniDicSchemaError,
        InvalidUnknownFeatureError,
    ):
        assert issubclass(exc_type, RomanizerCoreError)


def test_dictionary_not_found_error_message_includes_path():
    path = Path("/no/such/dict")
    error = DictionaryNotFoundError(path)
    assert error.path == path
    assert str(path) in str(error)


def test_invalid_dictionary_error_message_includes_path():
    path = Path("/some/file.txt")
    error = InvalidDictionaryError(path)
    assert error.path == path
    assert str(path) in str(error)


def test_span_resolution_error_message_includes_surface_and_cursor():
    error = SpanResolutionError(surface="猫", cursor=5)
    assert error.surface == "猫"
    assert error.cursor == 5
    assert "猫" in str(error)
    assert "5" in str(error)


def test_unsupported_schema_error_without_counts_reports_schema_id():
    error = UnsupportedUniDicSchemaError("unknown-schema-id")
    assert error.schema_id == "unknown-schema-id"
    assert "unknown-schema-id" in str(error)


def test_unsupported_schema_error_with_counts_reports_counts():
    error = UnsupportedUniDicSchemaError(
        "unidic-cwj-202512-29",
        expected=29,
        actual=28,
        surface="猫",
        feature="raw,feature,string",
    )
    assert error.expected == 29
    assert error.actual == 28
    assert "29" in str(error)
    assert "28" in str(error)


def test_invalid_unknown_feature_error_reports_counts():
    error = InvalidUnknownFeatureError(
        expected_at_least=6,
        actual=2,
        surface="Python",
        feature="名詞,普通名詞",
    )
    assert error.expected_at_least == 6
    assert error.actual == 2
    assert "6" in str(error)
    assert "2" in str(error)
