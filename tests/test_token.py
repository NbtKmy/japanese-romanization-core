import dataclasses

import pytest

from romanizer_core.models.token import Token


def _make_token(**overrides) -> Token:
    defaults = dict(
        id="t0",
        surface="猫",
        start=0,
        end=1,
        is_unknown=False,
        lemma="猫",
        lemma_reading="ネコ",
        pos=("名詞", "普通名詞", "一般"),
        conjugation_type=None,
        conjugation_form=None,
        orth="猫",
        kana="ネコ",
        pronunciation="ネコ",
        form="ネコ",
        form_base="ネコ",
        word_type="和",
    )
    defaults.update(overrides)
    return Token(**defaults)


def test_token_holds_all_fields():
    token = _make_token()
    assert token.id == "t0"
    assert token.surface == "猫"
    assert token.pos == ("名詞", "普通名詞", "一般")
    assert token.kana == "ネコ"
    assert token.is_unknown is False


def test_token_is_frozen():
    token = _make_token()
    with pytest.raises(dataclasses.FrozenInstanceError):
        token.surface = "犬"
