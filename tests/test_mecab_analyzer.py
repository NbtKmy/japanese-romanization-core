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


def _build_analyzer(dictionary_path):
    config = MeCabAnalyzerConfig(
        dictionary=DictionaryConfig(path=dictionary_path, version="202512"),
    )
    return MeCabAnalyzer(config)


def test_analyze_excludes_bos_eos_and_preserves_span_invariant(dictionary_path):
    analyzer = _build_analyzer(dictionary_path)

    result = analyzer.analyze("吾輩は猫である")

    assert len(result.tokens) > 0
    for token in result.tokens:
        assert result.text[token.start:token.end] == token.surface


def test_analyze_detects_kana_pronunciation_split_for_particle_ha(dictionary_path):
    analyzer = _build_analyzer(dictionary_path)

    result = analyzer.analyze("吾輩は猫である")

    ha_token = next(t for t in result.tokens if t.surface == "は")
    assert ha_token.kana == "ハ"
    assert ha_token.pronunciation == "ワ"


def test_analyze_marks_out_of_vocabulary_words_as_unknown(dictionary_path):
    analyzer = _build_analyzer(dictionary_path)

    result = analyzer.analyze("PythonでMeCabを使う")

    unknown_surfaces = {t.surface for t in result.tokens if t.is_unknown}
    assert "Python" in unknown_surfaces
    assert "MeCab" in unknown_surfaces


def test_analyze_empty_string_returns_no_tokens(dictionary_path):
    analyzer = _build_analyzer(dictionary_path)

    result = analyzer.analyze("")

    assert result.text == ""
    assert result.tokens == ()


def test_analyze_whitespace_only_preserves_text(dictionary_path):
    analyzer = _build_analyzer(dictionary_path)

    result = analyzer.analyze("   ")

    assert result.text == "   "


def test_analyze_repeated_surface_resolves_distinct_spans(dictionary_path):
    analyzer = _build_analyzer(dictionary_path)

    result = analyzer.analyze("猫猫猫")

    cat_tokens = [t for t in result.tokens if t.surface == "猫"]
    assert len(cat_tokens) == 3
    assert [(t.start, t.end) for t in cat_tokens] == [(0, 1), (1, 2), (2, 3)]
    for token in result.tokens:
        assert result.text[token.start:token.end] == token.surface
