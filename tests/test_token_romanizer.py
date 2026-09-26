from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1
from romanizer_core.models.token import Token
from romanizer_core.romanization.context_resolver import ContextResolver
from romanizer_core.romanization.long_vowel_resolver import LongVowelResolver
from romanizer_core.romanization.token_romanizer import TokenRomanizer


def _make_romanizer() -> TokenRomanizer:
    return TokenRomanizer(
        kana_romanizer=KanaRomanizer(MODIFIED_HEPBURN_V1),
        context_resolver=ContextResolver(),
        long_vowel_resolver=LongVowelResolver(),
    )


def _token(**overrides) -> Token:
    defaults = dict(
        id="t0",
        surface="_",
        start=0,
        end=1,
        is_unknown=False,
        lemma="_",
        lemma_reading="_",
        pos=(),
        conjugation_type=None,
        conjugation_form=None,
        orth="_",
        kana=None,
        pronunciation=None,
        form=None,
        form_base=None,
        word_type=None,
    )
    defaults.update(overrides)
    return Token(**defaults)


def test_romanizes_plain_noun_from_kana():
    romanizer = _make_romanizer()
    token = _token(id="t0", surface="猫", pos=("名詞",), kana="ネコ", orth="猫")
    result = romanizer.romanize([token])
    assert result[0].token_id == "t0"
    assert result[0].romaji == "neko"
    assert result[0].source == "kana"
    assert result[0].fuses_with_next is False


def test_particle_ha_overrides_to_wa():
    romanizer = _make_romanizer()
    token = _token(
        id="t1", surface="は", pos=("助詞", "係助詞"), kana="ハ", pronunciation="ワ"
    )
    result = romanizer.romanize([token])
    assert result[0].romaji == "wa"
    assert result[0].source == "pronunciation"


def test_particle_he_overrides_to_e():
    romanizer = _make_romanizer()
    token = _token(
        id="t1", surface="へ", pos=("助詞", "格助詞"), kana="ヘ", pronunciation="エ"
    )
    result = romanizer.romanize([token])
    assert result[0].romaji == "e"


def test_particle_wo_overrides_to_o():
    romanizer = _make_romanizer()
    token = _token(
        id="t1", surface="を", pos=("助詞", "格助詞"), kana="ヲ", pronunciation="オ"
    )
    result = romanizer.romanize([token])
    assert result[0].romaji == "o"


def test_non_particle_ha_is_not_overridden():
    # A word whose kana happens to be ハ but isn't a 助詞 must romanize
    # literally, not get the grammatical "wa" override.
    romanizer = _make_romanizer()
    token = _token(id="t0", surface="葉", pos=("名詞",), kana="ハ", pronunciation="ハ")
    result = romanizer.romanize([token])
    assert result[0].romaji == "ha"


def test_kana_none_falls_back_to_pronunciation():
    romanizer = _make_romanizer()
    token = _token(id="t0", surface="_", pos=("名詞",), kana=None, pronunciation="ネコ")
    result = romanizer.romanize([token])
    assert result[0].romaji == "neko"
    assert result[0].source == "pronunciation"


def test_kana_and_pronunciation_none_falls_back_to_literal_orth():
    romanizer = _make_romanizer()
    token = _token(
        id="t0", surface="。", pos=("補助記号", "句点"), kana=None, pronunciation=None, orth="。"
    )
    result = romanizer.romanize([token])
    assert result[0].romaji == "。"
    assert result[0].source == "orth"


def test_all_lexical_fields_none_falls_back_to_surface():
    romanizer = _make_romanizer()
    token = _token(
        id="t0",
        surface="ｘ",
        pos=(),
        is_unknown=True,
        lemma=None,
        lemma_reading=None,
        orth=None,
        kana=None,
        pronunciation=None,
        form=None,
        form_base=None,
        word_type=None,
    )
    result = romanizer.romanize([token])
    assert result[0].romaji == "ｘ"
    assert result[0].source == "surface"


def test_cross_token_sokuon_sets_fuses_with_next():
    romanizer = _make_romanizer()
    stem = _token(id="t0", surface="言っ", pos=("動詞",), kana="イッ")
    ending = _token(id="t1", surface="た", pos=("助動詞",), kana="タ")
    result = romanizer.romanize([stem, ending])
    assert result[0].romaji == "it"
    assert result[0].fuses_with_next is True
    assert result[1].romaji == "ta"
    assert result[1].fuses_with_next is False


def test_absolute_final_sokuon_does_not_fuse():
    romanizer = _make_romanizer()
    token = _token(id="t0", surface="あっ", pos=("感動詞",), kana="アッ")
    result = romanizer.romanize([token])
    assert result[0].romaji == "a'"
    assert result[0].fuses_with_next is False


def test_godan_verb_long_vowel_correction_applies_in_full_pipeline():
    romanizer = _make_romanizer()
    token = _token(
        id="t0",
        surface="食う",
        pos=("動詞", "一般"),
        conjugation_type="五段-ワア行",
        conjugation_form="終止形-一般",
        kana="クウ",
    )
    result = romanizer.romanize([token])
    assert result[0].romaji == "kuu"
