import json

from romanizer_core.models.analysis import AnalyzerInfo, DictionaryInfo
from romanizer_core.models.romanization_result import RomanizationResult
from romanizer_core.models.romanization_scheme import RomanizationScheme
from romanizer_core.models.romanized_token import RomanizedToken
from romanizer_core.models.token import Token
from romanizer_core.serialization import romanization_to_dict


def _sample_result() -> RomanizationResult:
    dictionary = DictionaryInfo(
        name="unidic-cwj", version="202512", schema_id="unidic-cwj-202512-29"
    )
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
    romanized_token = RomanizedToken(
        token_id="t0", romaji="neko", source="kana", fuses_with_next=False
    )
    return RomanizationResult(
        text="猫",
        romanized_text="Neko",
        romanization_scheme=RomanizationScheme(name="modified_hepburn", version="1"),
        analyzer=analyzer,
        tokens=(token,),
        romanized_tokens=(romanized_token,),
    )


def test_romanization_to_dict_matches_expected_shape():
    data = romanization_to_dict(_sample_result())

    assert data["json_schema_version"] == "1"
    assert data["text"] == "猫"
    assert data["romanized_text"] == "Neko"
    assert data["romanization_scheme"] == {"name": "modified_hepburn", "version": "1"}
    assert data["analyzer"]["name"] == "mecab"
    assert data["analyzer"]["dictionary"]["schema_id"] == "unidic-cwj-202512-29"


def test_romanization_to_dict_nests_romanization_under_each_token():
    data = romanization_to_dict(_sample_result())

    token_dict = data["tokens"][0]
    assert token_dict["surface"] == "猫"
    assert token_dict["romanization"] == {
        "romaji": "neko",
        "source": "kana",
        "fuses_with_next": False,
    }


def test_romanization_to_dict_is_json_serializable():
    data = romanization_to_dict(_sample_result())

    serialized = json.dumps(data, ensure_ascii=False)
    assert "neko" in serialized


def test_romanization_to_dict_raises_key_error_on_misaligned_token_id():
    result = _sample_result()
    mismatched = RomanizationResult(
        text=result.text,
        romanized_text=result.romanized_text,
        romanization_scheme=result.romanization_scheme,
        analyzer=result.analyzer,
        tokens=result.tokens,
        romanized_tokens=(
            RomanizedToken(token_id="wrong-id", romaji="neko", source="kana"),
        ),
    )

    try:
        romanization_to_dict(mismatched)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError for a token_id with no matching Token")
