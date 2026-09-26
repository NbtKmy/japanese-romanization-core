from romanizer_core.models.kana_romanization import KanaRomanization
from romanizer_core.models.token import Token
from romanizer_core.romanization.long_vowel_resolver import LongVowelResolver

resolver = LongVowelResolver()


def _godan_verb_token(*, kana: str) -> Token:
    return Token(
        id="t0",
        surface="_",
        start=0,
        end=1,
        is_unknown=False,
        lemma="_",
        lemma_reading="_",
        pos=("動詞", "一般"),
        conjugation_type="五段-ワア行",
        conjugation_form="終止形-一般",
        orth="_",
        kana=kana,
        pronunciation=kana,
        form=kana,
        form_base=kana,
        word_type="和",
    )


def test_reverts_uu_contraction_for_godan_verb_kuu_taberu_food_verb():
    # 食う (kuu): KanaRomanizer's default same-vowel contraction wrongly
    # produces "kū"; the verb's dictionary-form-final う is not a chōonpu.
    token = _godan_verb_token(kana="クウ")
    kr = KanaRomanization(text="kū", final_vowel="ū")
    result = resolver.resolve(token=token, kana_romanization=kr)
    assert result.text == "kuu"
    assert result.final_vowel == "u"


def test_reverts_ou_historical_contraction_for_godan_verb_tou():
    # 問う (tou): default ou->ō historical contraction wrongly produces "tō".
    token = _godan_verb_token(kana="トウ")
    kr = KanaRomanization(text="tō", final_vowel="ō")
    result = resolver.resolve(token=token, kana_romanization=kr)
    assert result.text == "tou"
    assert result.final_vowel == "u"


def test_reverts_ou_contraction_mid_word_for_godan_verb_sasou():
    # 誘う (sasou): contraction happens on the second-to-last mora, not the
    # last character of the whole string.
    token = _godan_verb_token(kana="サソウ")
    kr = KanaRomanization(text="sasō", final_vowel="ō")
    result = resolver.resolve(token=token, kana_romanization=kr)
    assert result.text == "sasou"


def test_does_not_revert_ou_contraction_for_volitional_form_ikou():
    # 行こう (ikō, 意志推量形/volitional "let's go"): a genuine chōonpu, not
    # the verb's dictionary-final う. Real UniDic tokenizes this as ONE
    # token (cType=五段-カ行, cForm=意志推量形, kana=イコウ) -- the same
    # kana-ends-in-ウ shape as 問う, but here the contraction is correct
    # and must not be reverted.
    token = Token(
        id="t0",
        surface="行こう",
        start=0,
        end=3,
        is_unknown=False,
        lemma="行く",
        lemma_reading="イク",
        pos=("動詞", "非自立可能"),
        conjugation_type="五段-カ行",
        conjugation_form="意志推量形",
        orth="行こう",
        kana="イコウ",
        pronunciation="イコー",
        form="イコウ",
        form_base="イコウ",
        word_type="和",
    )
    kr = KanaRomanization(text="ikō", final_vowel="ō")
    result = resolver.resolve(token=token, kana_romanization=kr)
    assert result is kr


def test_noop_when_no_contraction_happened_kau():
    # 買う (kau): あ+う never contracts, final_vowel is plain "u"; nothing to revert.
    token = _godan_verb_token(kana="カウ")
    kr = KanaRomanization(text="kau", final_vowel="u")
    result = resolver.resolve(token=token, kana_romanization=kr)
    assert result is kr


def test_noop_for_non_godan_token_even_if_kana_ends_in_u():
    # 小躍り (koodori, compound noun): no conjugation_type at all. This is
    # the documented v1 limitation (kana_romanizer_spec.md §44) -- compound
    # lexical-boundary detection is out of scope, so we must not guess.
    token = Token(
        id="t0",
        surface="小躍り",
        start=0,
        end=3,
        is_unknown=False,
        lemma="小躍り",
        lemma_reading="コオドリ",
        pos=("名詞", "普通名詞"),
        conjugation_type=None,
        conjugation_form=None,
        orth="小躍り",
        kana="コオドリ",
        pronunciation="コオドリ",
        form="コオドリ",
        form_base="コオドリ",
        word_type="和",
    )
    kr = KanaRomanization(text="kōdori", final_vowel="ō")
    result = resolver.resolve(token=token, kana_romanization=kr)
    assert result is kr


def test_noop_for_godan_verb_whose_kana_does_not_end_in_u():
    # 言っ (連用形-促音便): still a 五段 verb, but this form ends in っ, not う.
    token = Token(
        id="t0",
        surface="言っ",
        start=0,
        end=2,
        is_unknown=False,
        lemma="言う",
        lemma_reading="イウ",
        pos=("動詞", "一般"),
        conjugation_type="五段-ワア行",
        conjugation_form="連用形-促音便",
        orth="言っ",
        kana="イッ",
        pronunciation="イッ",
        form="イッ",
        form_base="イウ",
        word_type="和",
    )
    kr = KanaRomanization(text="i", pending_sokuon=True)
    result = resolver.resolve(token=token, kana_romanization=kr)
    assert result is kr
