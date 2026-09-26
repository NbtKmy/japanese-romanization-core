from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


def test_unvoiced_hiragana_iteration_mark_repeats_preceding_mora():
    # かゝ -> "kaka"
    assert romanizer.romanize("かゝ").text == "kaka"


def test_unvoiced_katakana_iteration_mark_repeats_preceding_mora():
    assert romanizer.romanize("かヽ").text == "kaka"


def test_voiced_hiragana_iteration_mark_repeats_with_dakuten():
    # すゞき -> "suzuki"
    assert romanizer.romanize("すゞき").text == "suzuki"


def test_voiced_katakana_iteration_mark_repeats_with_dakuten():
    assert romanizer.romanize("すヾき").text == "suzuki"


def test_leading_iteration_mark_is_preserved_without_crashing():
    result = romanizer.romanize("ゝ")
    assert result.text == "ゝ"


def test_voiced_mark_after_mora_without_voiced_counterpart_is_preserved():
    # あ has no voiced counterpart, so ゞ can't repeat it voiced.
    result = romanizer.romanize("あゞ")
    assert result.text == "aゞ"


def test_kanji_iteration_marks_are_not_special_cased_and_pass_through():
    # 々/〃 are never added to any mapping table, so they fall through to
    # the generic preserve-fallback automatically (spec §46) — no dedicated
    # handling needed.
    assert romanizer.romanize("々").text == "々"
    assert romanizer.romanize("〃").text == "〃"
