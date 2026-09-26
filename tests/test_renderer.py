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
    assert renderer.render(tokens, romanized) == "「Neko」"


def test_capitalizes_first_letter_even_when_first_token_is_punctuation():
    tokens = [
        _token(id="t0", pos=("補助記号", "括弧開")),
        _token(id="t1", pos=("名詞",)),
    ]
    romanized = [
        RomanizedToken(token_id="t0", romaji="「", source="orth"),
        RomanizedToken(token_id="t1", romaji="neko", source="kana"),
    ]
    assert renderer.render(tokens, romanized) == "「Neko"


def test_fuses_with_next_suppresses_space():
    tokens = [_token(id="t0", pos=("動詞",)), _token(id="t1", pos=("助動詞",))]
    romanized = [
        RomanizedToken(token_id="t0", romaji="it", source="kana", fuses_with_next=True),
        RomanizedToken(token_id="t1", romaji="ta", source="kana"),
    ]
    assert renderer.render(tokens, romanized) == "Itta"


def test_capitalizes_first_letter_of_each_sentence_after_a_period():
    tokens = [
        _token(id="t0", pos=("名詞",)),
        _token(id="t1", pos=("助動詞",)),
        _token(id="t2", pos=("補助記号", "句点")),
        _token(id="t3", pos=("名詞",)),
        _token(id="t4", pos=("助動詞",)),
        _token(id="t5", pos=("補助記号", "句点")),
    ]
    romanized = [
        RomanizedToken(token_id="t0", romaji="neko", source="kana"),
        RomanizedToken(token_id="t1", romaji="da", source="kana"),
        RomanizedToken(token_id="t2", romaji="。", source="orth"),
        RomanizedToken(token_id="t3", romaji="inu", source="kana"),
        RomanizedToken(token_id="t4", romaji="da", source="kana"),
        RomanizedToken(token_id="t5", romaji="。", source="orth"),
    ]
    assert renderer.render(tokens, romanized) == "Neko da。 Inu da。"


def test_does_not_capitalize_past_a_leading_digit_token():
    # "1000円です。" -- the sentence-initial position is occupied by a
    # digit token, which has no case; the following word must not be
    # capitalized just because it happens to be the first *letter*.
    tokens = [
        _token(id="t0", pos=("名詞", "数詞")),
        _token(id="t1", pos=("名詞",)),
        _token(id="t2", pos=("助動詞",)),
        _token(id="t3", pos=("補助記号", "句点")),
    ]
    romanized = [
        RomanizedToken(token_id="t0", romaji="1000", source="surface"),
        RomanizedToken(token_id="t1", romaji="en", source="kana"),
        RomanizedToken(token_id="t2", romaji="desu", source="kana"),
        RomanizedToken(token_id="t3", romaji="。", source="orth"),
    ]
    assert renderer.render(tokens, romanized) == "1000 en desu。"


def test_whitespace_token_becomes_a_single_separator_not_literal_text():
    # 山田　太郎 -- a UniDic 空白 token between two name tokens must not
    # render its literal full-width space character with extra spaces
    # stacked around it.
    tokens = [
        _token(id="t0", pos=("名詞", "固有名詞")),
        _token(id="t1", pos=("空白",)),
        _token(id="t2", pos=("名詞", "固有名詞")),
    ]
    romanized = [
        RomanizedToken(token_id="t0", romaji="yamada", source="kana"),
        RomanizedToken(token_id="t1", romaji="　", source="orth"),
        RomanizedToken(token_id="t2", romaji="tarō", source="kana"),
    ]
    assert renderer.render(tokens, romanized) == "Yamada tarō"


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
