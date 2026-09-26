from romanizer_core.models.analysis import AnalyzerInfo, DictionaryInfo
from romanizer_core.models.romanization_result import RomanizationResult
from romanizer_core.models.romanization_scheme import RomanizationScheme
from romanizer_core.models.romanized_token import RomanizedToken
from romanizer_core.models.token import Token


def _sample_token() -> Token:
    return Token(
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


def test_romanization_result_holds_all_fields():
    analyzer = AnalyzerInfo(
        name="mecab",
        version="0.996",
        dictionary=DictionaryInfo(
            name="unidic-cwj", version="202512", schema_id="unidic-cwj-202512-29"
        ),
    )
    token = _sample_token()
    romanized_token = RomanizedToken(token_id="t0", romaji="neko", source="kana")

    result = RomanizationResult(
        text="猫",
        romanized_text="Neko",
        romanization_scheme=RomanizationScheme(name="modified_hepburn", version="1"),
        analyzer=analyzer,
        tokens=(token,),
        romanized_tokens=(romanized_token,),
    )

    assert result.text == "猫"
    assert result.romanized_text == "Neko"
    assert result.romanization_scheme.name == "modified_hepburn"
    assert result.analyzer.name == "mecab"
    assert result.tokens == (token,)
    assert result.romanized_tokens == (romanized_token,)


def test_romanization_result_is_frozen():
    analyzer = AnalyzerInfo(
        name="mecab",
        version="0.996",
        dictionary=DictionaryInfo(
            name="unidic-cwj", version="202512", schema_id="unidic-cwj-202512-29"
        ),
    )
    result = RomanizationResult(
        text="猫",
        romanized_text="Neko",
        romanization_scheme=RomanizationScheme(name="modified_hepburn", version="1"),
        analyzer=analyzer,
        tokens=(),
        romanized_tokens=(),
    )
    try:
        result.romanized_text = "Inu"  # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("expected AttributeError on mutation")
