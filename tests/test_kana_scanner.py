from romanizer_core.kana.scanner import longest_match

LOOKUP = {
    "a": "1char",
    "ab": "2char",
    "abc": "3char",
    "x": "single-x",
}


def test_prefers_three_char_match_over_shorter():
    assert longest_match("abcd", 0, LOOKUP) == ("abc", "3char")


def test_prefers_two_char_match_when_three_char_unavailable():
    assert longest_match("abd", 0, LOOKUP) == ("ab", "2char")


def test_falls_back_to_one_char_match():
    assert longest_match("axyz", 1, LOOKUP) == ("x", "single-x")


def test_returns_none_when_nothing_matches():
    assert longest_match("zzz", 0, LOOKUP) is None


def test_returns_none_at_end_of_string():
    assert longest_match("a", 1, LOOKUP) is None


def test_match_near_end_of_string_only_tries_available_lengths():
    assert longest_match("xa", 1, LOOKUP) == ("a", "1char")
