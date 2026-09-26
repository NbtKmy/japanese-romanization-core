import pytest

from romanizer_core import (
    DictionaryConfig,
    MeCabAnalyzer,
    MeCabAnalyzerConfig,
)
from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1
from romanizer_core.romanization.context_resolver import ContextResolver
from romanizer_core.romanization.long_vowel_resolver import LongVowelResolver
from romanizer_core.romanization.renderer import Renderer
from romanizer_core.romanization.token_romanizer import TokenRomanizer


def _build_pipeline(dictionary_path):
    analyzer = MeCabAnalyzer(
        MeCabAnalyzerConfig(
            dictionary=DictionaryConfig(path=dictionary_path, version="202512")
        )
    )
    token_romanizer = TokenRomanizer(
        kana_romanizer=KanaRomanizer(MODIFIED_HEPBURN_V1),
        context_resolver=ContextResolver(),
        long_vowel_resolver=LongVowelResolver(),
    )
    renderer = Renderer()
    return analyzer, token_romanizer, renderer


def _romanize(analyzer, token_romanizer, renderer, text: str) -> str:
    analysis = analyzer.analyze(text)
    romanized_tokens = token_romanizer.romanize(analysis.tokens)
    return renderer.render(analysis.tokens, romanized_tokens)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("吾輩は猫である。", "Wagahai wa neko de aru。"),
        ("学校へ行く", "Gakkō e iku"),
        ("水を飲む", "Mizu o nomu"),
        ("「猫」と言った。", "「Neko」 to itta。"),
    ],
)
def test_full_pipeline_matches_expected_romanization(
    dictionary_path, text, expected
):
    analyzer, token_romanizer, renderer = _build_pipeline(dictionary_path)
    assert _romanize(analyzer, token_romanizer, renderer, text) == expected


@pytest.mark.parametrize(
    ("verb_text", "expected"),
    [
        ("食う", "Kuu"),
        ("問う", "Tou"),
        ("誘う", "Sasou"),
        ("買う", "Kau"),
    ],
)
def test_godan_verb_final_u_is_never_treated_as_a_choonpu(
    dictionary_path, verb_text, expected
):
    analyzer, token_romanizer, renderer = _build_pipeline(dictionary_path)
    assert _romanize(analyzer, token_romanizer, renderer, verb_text) == expected


def test_known_compound_lexical_boundary_limitation_is_documented(dictionary_path):
    # 小躍り (koodori) is a documented v1 limitation: KanaRomanizer's default
    # same-vowel contraction fires and LongVowelResolver has no compound-
    # boundary information to revert it (kana_romanizer_spec.md §44). This
    # test pins the *current* (known-imperfect) behavior so a future fix is
    # a deliberate, visible change rather than a silent regression.
    analyzer, token_romanizer, renderer = _build_pipeline(dictionary_path)
    assert _romanize(analyzer, token_romanizer, renderer, "小躍り") == "Kōdori"
