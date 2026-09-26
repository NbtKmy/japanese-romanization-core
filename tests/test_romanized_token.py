from romanizer_core.models.romanized_token import RomanizedToken


def test_romanized_token_defaults_fuses_with_next_to_false():
    token = RomanizedToken(token_id="t0", romaji="neko", source="kana")
    assert token.fuses_with_next is False


def test_romanized_token_is_frozen():
    token = RomanizedToken(token_id="t0", romaji="neko", source="kana")
    try:
        token.romaji = "inu"  # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("expected AttributeError on mutation")
