from romanizer_core.models.romanized_token import RomanizedToken
from romanizer_core.models.token import Token
from romanizer_core.romanization.renderer import Renderer

renderer = Renderer()


def _token(**overrides) -> Token:
    defaults = dict(
        id="t0",
        surface="_",
        start=0,
        end=1,
        is_unknown=False,
        lemma=None,
        lemma_reading=None,
        pos=(),
        conjugation_type=None,
        conjugation_form=None,
        orth=None,
        kana=None,
        pronunciation=None,
        form=None,
        form_base=None,
        word_type=None,
    )
    defaults.update(overrides)
    return Token(**defaults)


def test_empty_sequences_render_to_empty_string():
    assert renderer.render([], []) == ""


def test_words_are_space_joined_and_first_letter_capitalized():
    tokens = [
        _token(id="t0", pos=("代名詞",)),
        _token(id="t1", pos=("助詞",)),
        _token(id="t2", pos=("名詞",)),
    ]
    romanized = [
        RomanizedToken(token_id="t0", romaji="wagahai", source="kana"),
        RomanizedToken(token_id="t1", romaji="wa", source="pronunciation"),
        RomanizedToken(token_id="t2", romaji="neko", source="kana"),
    ]
    assert renderer.render(tokens, romanized) == "Wagahai wa neko"


def test_closing_punctuation_has_no_leading_space():
    tokens = [
        _token(id="t0", pos=("名詞",)),
        _token(id="t1", pos=("補助記号", "句点")),
    ]
    romanized = [
        RomanizedToken(token_id="t0", romaji="neko", source="kana"),
        RomanizedToken(token_id="t1", romaji="。", source="orth"),
    ]
    assert renderer.render(tokens, romanized) == "Neko。"


def test_opening_bracket_has_no_trailing_space():
    tokens = [
        _token(id="t0", pos=("補助記号", "括弧開")),
        _token(id="t1", pos=("名詞",)),
        _token(id="t2", pos=("補助記号", "括弧閉")),
    ]
    romanized = [
        RomanizedToken(token_id="t0", romaji="「", source="orth"),
        RomanizedToken(token_id="t1", romaji="neko", source="kana"),
        RomanizedToken(token_id="t2", romaji="」", source="orth"),
    ]
    assert renderer.render(tokens, romanized) == "「neko」"


def test_fuses_with_next_suppresses_space():
    tokens = [_token(id="t0", pos=("動詞",)), _token(id="t1", pos=("助動詞",))]
    romanized = [
        RomanizedToken(token_id="t0", romaji="it", source="kana", fuses_with_next=True),
        RomanizedToken(token_id="t1", romaji="ta", source="kana"),
    ]
    assert renderer.render(tokens, romanized) == "Itta"


def test_empty_romaji_token_is_skipped_without_extra_space():
    tokens = [
        _token(id="t0", pos=("名詞",)),
        _token(id="t1", pos=()),
        _token(id="t2", pos=("名詞",)),
    ]
    romanized = [
        RomanizedToken(token_id="t0", romaji="neko", source="kana"),
        RomanizedToken(token_id="t1", romaji="", source="surface"),
        RomanizedToken(token_id="t2", romaji="inu", source="kana"),
    ]
    assert renderer.render(tokens, romanized) == "Neko inu"
