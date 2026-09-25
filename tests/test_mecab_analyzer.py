import pytest

from romanizer_core.analyzer.config import DictionaryConfig, MeCabAnalyzerConfig
from romanizer_core.analyzer.mecab import MeCabAnalyzer
from romanizer_core.exceptions import DictionaryNotFoundError, InvalidDictionaryError


def test_analyzer_initializes_and_reports_info(dictionary_path):
    config = MeCabAnalyzerConfig(
        dictionary=DictionaryConfig(path=dictionary_path, version="202512"),
    )

    analyzer = MeCabAnalyzer(config)

    assert analyzer.info.name == "mecab"
    assert analyzer.info.version == "0.996"
    assert analyzer.info.dictionary.name == "unidic-cwj"
    assert analyzer.info.dictionary.version == "202512"
    assert analyzer.info.dictionary.schema_id == "unidic-cwj-202512-29"


def test_analyzer_raises_dictionary_not_found_for_missing_path(tmp_path):
    missing = tmp_path / "does-not-exist"
    config = MeCabAnalyzerConfig(dictionary=DictionaryConfig(path=missing))

    with pytest.raises(DictionaryNotFoundError):
        MeCabAnalyzer(config)


def test_analyzer_raises_invalid_dictionary_for_non_directory(tmp_path):
    file_path = tmp_path / "not-a-directory"
    file_path.write_text("not a dictionary")
    config = MeCabAnalyzerConfig(dictionary=DictionaryConfig(path=file_path))

    with pytest.raises(InvalidDictionaryError):
        MeCabAnalyzer(config)
