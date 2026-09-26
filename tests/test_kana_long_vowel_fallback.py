"""KanaRomanizer's default (Token-free) long-vowel contraction (spec §41/§42/§56).

Spec §56 lists mandatory KanaRomanizer-level cases that require default
same-vowel / historical ou->ō contraction (asserted below), and separately
carves out lexical-boundary / verb-morphology exceptions (くう->kuu,
こおどり->koodori) as LongVowelResolver's responsibility, out of scope for
this layer. KanaRomanizer's uncorrected default output for those exception
words is asserted too, so a future LongVowelResolver has a documented
starting point to correct from.

Note: KanaRomanizer never capitalizes output (title casing is Renderer's
job per spec §46/Part XVI item 12), so proper-noun examples from the spec
(Ōsaka, Tōkyō) are asserted here in lowercase.
"""

import pytest

from romanizer_core.kana.romanizer import KanaRomanizer
from romanizer_core.kana.scheme import MODIFIED_HEPBURN_V1

romanizer = KanaRomanizer(MODIFIED_HEPBURN_V1)


@pytest.mark.parametrize(
    ("kana", "expected"),
    [
        ("にいさん", "niisan"),
        ("すうがく", "sūgaku"),
        ("おねえさん", "onēsan"),
        ("おおさか", "ōsaka"),
        ("がっこう", "gakkō"),
        ("とうきょう", "tōkyō"),
        ("せいふく", "seifuku"),
    ],
)
def test_mandatory_default_long_vowel_cases(kana, expected):
    assert romanizer.romanize(kana).text == expected


@pytest.mark.parametrize(
    ("kana", "kana_romanizer_default"),
    [
        # くう -> kuu is the correct Hepburn form (u-verb "食う"), but
        # KanaRomanizer has no verb-morphology information and applies the
        # same-vowel default, producing "kū". LongVowelResolver (Token
        # dependent, future phase) is responsible for reverting this.
        ("くう", "kū"),
        # こおどり -> koodori is a lexical-boundary exception (小躍り);
        # KanaRomanizer's default same-vowel contraction produces "kōdori".
        ("こおどり", "kōdori"),
    ],
)
def test_lexical_exceptions_are_not_handled_by_kana_romanizer_alone(
    kana, kana_romanizer_default
):
    assert romanizer.romanize(kana).text == kana_romanizer_default
