from romanizer_core import DictionaryConfig, MeCabAnalyzer, MeCabAnalyzerConfig
from romanizer_core.models.romanization_result import RomanizationResult
from romanizer_core.romanizer import Romanizer


def _build_analyzer(dictionary_path):
    return MeCabAnalyzer(
        MeCabAnalyzerConfig(
            dictionary=DictionaryConfig(path=dictionary_path, version="202512")
        )
    )


def test_modified_hepburn_romanizes_matching_existing_pipeline_output(dictionary_path):
    romanizer = Romanizer.modified_hepburn(_build_analyzer(dictionary_path))

    result = romanizer.romanize("吾輩は猫である。")

    assert isinstance(result, RomanizationResult)
    assert result.text == "吾輩は猫である。"
    assert result.romanized_text == "Wagahai wa neko de aru。"


def test_result_tokens_and_romanized_tokens_are_aligned(dictionary_path):
    romanizer = Romanizer.modified_hepburn(_build_analyzer(dictionary_path))

    result = romanizer.romanize("吾輩は猫である。")

    assert len(result.tokens) == len(result.romanized_tokens)
    for token, romanized_token in zip(result.tokens, result.romanized_tokens):
        assert romanized_token.token_id == token.id


def test_romanization_scheme_matches_the_kana_scheme_actually_used(dictionary_path):
    from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

    romanizer = Romanizer.modified_hepburn(_build_analyzer(dictionary_path))
    result = romanizer.romanize("猫")

    assert result.romanization_scheme.name == MODIFIED_HEPBURN_V1.name
    assert result.romanization_scheme.version == MODIFIED_HEPBURN_V1.version


def test_empty_string_romanizes_to_empty_result(dictionary_path):
    romanizer = Romanizer.modified_hepburn(_build_analyzer(dictionary_path))

    result = romanizer.romanize("")

    assert result.text == ""
    assert result.romanized_text == ""
    assert result.tokens == ()
    assert result.romanized_tokens == ()


def test_analyzer_info_is_carried_through(dictionary_path):
    analyzer = _build_analyzer(dictionary_path)
    romanizer = Romanizer.modified_hepburn(analyzer)

    result = romanizer.romanize("猫")

    assert result.analyzer.name == "mecab"
    assert result.analyzer.dictionary.name == "unidic-cwj"
