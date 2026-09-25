from romanizer_core.models.analysis import AnalysisResult, AnalyzerInfo, DictionaryInfo
from romanizer_core.models.token import Token


def test_analysis_result_holds_text_analyzer_and_tokens():
    dictionary = DictionaryInfo(name="unidic-cwj", version="202512", schema_id="unidic-cwj-202512-29")
    analyzer = AnalyzerInfo(name="mecab", version="0.996", dictionary=dictionary)
    token = Token(
        id="t0",
        surface="猫",
        start=0,
        end=1,
        is_unknown=False,
        lemma="猫",
        lemma_reading="ネコ",
        pos=("名詞",),
        conjugation_type=None,
        conjugation_form=None,
        orth="猫",
        kana="ネコ",
        pronunciation="ネコ",
        form="ネコ",
        form_base="ネコ",
        word_type="和",
    )

    result = AnalysisResult(text="猫", analyzer=analyzer, tokens=(token,))

    assert result.text == "猫"
    assert result.analyzer.dictionary.version == "202512"
    assert result.tokens == (token,)


def test_dictionary_info_allows_none_version():
    info = DictionaryInfo(name="unidic-cwj", version=None, schema_id="unidic-cwj-202512-29")
    assert info.version is None
