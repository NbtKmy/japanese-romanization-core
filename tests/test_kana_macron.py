from romanizer_core.kana.macron import MACRON, MACRON_TO_VOWEL


def test_macron_to_vowel_is_exact_reverse_of_macron():
    assert MACRON_TO_VOWEL == {macron: vowel for vowel, macron in MACRON.items()}


def test_macron_to_vowel_round_trips():
    for vowel, macron in MACRON.items():
        assert MACRON_TO_VOWEL[macron] == vowel
