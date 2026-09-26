from romanizer_core.models.kana_romanization import KanaRomanization
from romanizer_core.romanization.context_resolver import ContextResolver

resolver = ContextResolver()


def test_pending_sokuon_takes_next_tokens_initial_consonant():
    current = KanaRomanization(text="i", pending_sokuon=True)
    following = KanaRomanization(text="ta")
    result = resolver.resolve([current, following])
    assert result[0].text == "it"
    assert result[0].pending_sokuon is False
    assert result[1].text == "ta"


def test_pending_sokuon_before_ch_uses_t_prefix():
    current = KanaRomanization(text="ma", pending_sokuon=True)
    following = KanaRomanization(text="cha")
    result = resolver.resolve([current, following])
    assert result[0].text == "mat"


def test_pending_sokuon_with_no_next_token_gets_abrupt_apostrophe():
    current = KanaRomanization(text="a", pending_sokuon=True)
    result = resolver.resolve([current])
    assert result[0].text == "a'"
    assert result[0].pending_sokuon is False


def test_pending_sokuon_before_non_phonetic_next_slot_gets_abrupt_apostrophe():
    current = KanaRomanization(text="a", pending_sokuon=True)
    result = resolver.resolve([current, None])
    assert result[0].text == "a'"
    assert result[1] is None


def test_pending_syllabic_n_before_vowel_gets_apostrophe():
    current = KanaRomanization(text="kin", pending_syllabic_n=True)
    following = KanaRomanization(text="ichi")
    result = resolver.resolve([current, following])
    assert result[0].text == "kin'"
    assert result[0].pending_syllabic_n is False


def test_pending_syllabic_n_before_y_gets_apostrophe():
    current = KanaRomanization(text="kin", pending_syllabic_n=True)
    following = KanaRomanization(text="yōbi")
    result = resolver.resolve([current, following])
    assert result[0].text == "kin'"


def test_pending_syllabic_n_before_consonant_stays_plain():
    current = KanaRomanization(text="kan", pending_syllabic_n=True)
    following = KanaRomanization(text="pai")
    result = resolver.resolve([current, following])
    assert result[0].text == "kan"
    assert result[0].pending_syllabic_n is False


def test_pending_syllabic_n_with_no_next_token_stays_plain():
    current = KanaRomanization(text="kan", pending_syllabic_n=True)
    result = resolver.resolve([current])
    assert result[0].text == "kan"
    assert result[0].pending_syllabic_n is False


def test_non_pending_entries_pass_through_unchanged():
    current = KanaRomanization(text="neko")
    result = resolver.resolve([current])
    assert result[0] is current


def test_none_slots_pass_through_unchanged():
    result = resolver.resolve([None, KanaRomanization(text="neko")])
    assert result[0] is None
