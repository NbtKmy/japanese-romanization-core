from romanizer_core.kana.prepare import prepare_kana


def test_hiragana_input_is_unchanged():
    assert prepare_kana("がっこう") == "がっこう"


def test_katakana_is_converted_to_hiragana():
    assert prepare_kana("タクシー") == "たくしー"


def test_katakana_u_with_dakuten_becomes_hiragana_vu():
    assert prepare_kana("ヴァイオリン") == "ゔぁいおりん"


def test_katakana_iteration_marks_are_outside_conversion_range_and_pass_through():
    # ヽ/ヾ sit just past the ア..ヶ block that gets shifted to hiragana, so
    # they pass through unchanged; the romanizer's iteration-mark handling
    # accepts both the katakana and hiragana spellings directly.
    assert prepare_kana("ヽ") == "ヽ"
    assert prepare_kana("ヾ") == "ヾ"


def test_prolonged_sound_mark_is_not_shifted():
    assert prepare_kana("ー") == "ー"


def test_half_width_katakana_plain():
    assert prepare_kana("ｶﾆ") == "かに"


def test_half_width_katakana_with_dakuten():
    assert prepare_kana("ｶﾞｷﾞｸﾞｹﾞｺﾞ") == "がぎぐげご"


def test_half_width_katakana_with_handakuten():
    assert prepare_kana("ﾊﾟﾋﾟﾌﾟﾍﾟﾎﾟ") == "ぱぴぷぺぽ"


def test_half_width_u_with_dakuten_becomes_vu():
    assert prepare_kana("ｳﾞ") == "ゔ"


def test_half_width_prolonged_sound_mark_becomes_full_width():
    assert prepare_kana("ｶｰﾄﾆﾑ") == "かーとにむ"  # noqa: RUF001


def test_original_string_object_is_not_mutated():
    original = "タクシー"
    result = prepare_kana(original)
    assert original == "タクシー"
    assert result is not original


def test_ascii_and_unknown_characters_pass_through():
    assert prepare_kana("かなA1") == "かなA1"
