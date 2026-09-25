import json

from romanizer_core.models.analysis import AnalysisResult, AnalyzerInfo, DictionaryInfo
from romanizer_core.models.token import Token
from romanizer_core.serialization import analysis_to_dict


def _sample_result() -> AnalysisResult:
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
        pos=("名詞", "普通名詞", "一般"),
        conjugation_type=None,
        conjugation_form=None,
        orth="猫",
        kana="ネコ",
        pronunciation="ネコ",
        form="ネコ",
        form_base="ネコ",
        word_type="和",
    )
    return AnalysisResult(text="猫", analyzer=analyzer, tokens=(token,))


def test_analysis_to_dict_matches_expected_shape():
    result = _sample_result()

    data = analysis_to_dict(result)

    assert data["text"] == "猫"
    assert data["analyzer"]["name"] == "mecab"
    assert data["analyzer"]["dictionary"]["schema_id"] == "unidic-cwj-202512-29"
    assert data["tokens"][0]["surface"] == "猫"
    assert data["tokens"][0]["pos"] == ["名詞", "普通名詞", "一般"]


def test_analysis_to_dict_is_json_serializable():
    result = _sample_result()

    data = analysis_to_dict(result)

    serialized = json.dumps(data, ensure_ascii=False)
    assert "猫" in serialized
