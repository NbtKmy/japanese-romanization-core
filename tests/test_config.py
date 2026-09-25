from pathlib import Path

from romanizer_core.analyzer.config import DictionaryConfig, MeCabAnalyzerConfig


def test_dictionary_config_defaults():
    config = DictionaryConfig(path=Path("/path/to/unidic-cwj"))
    assert config.name == "unidic-cwj"
    assert config.version is None
    assert config.schema_id == "unidic-cwj-202512-29"


def test_mecab_analyzer_config_defaults_validate_dictionary_true():
    dictionary = DictionaryConfig(path=Path("/path/to/unidic-cwj"))
    config = MeCabAnalyzerConfig(dictionary=dictionary)
    assert config.validate_dictionary is True
    assert config.dictionary is dictionary
