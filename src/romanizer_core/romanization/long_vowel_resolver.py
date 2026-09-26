"""Corrects lexical/morphological long-vowel exceptions that KanaRomanizer's
kana-local default cannot know about (kana_romanizer_spec.md §43/§44).
"""

from dataclasses import replace

from ..kana.macron import MACRON_TO_VOWEL
from ..models.kana_romanization import KanaRomanization
from ..models.token import Token

_GODAN_PREFIX = "五段"
_VERB_FINAL_U_KANA = ("う", "ウ")
# Only 終止形/連体形 (dictionary/attributive form) genuinely end in the
# verb's own う. 意志推量形 (volitional, e.g. 行こう "ikō") also ends in ウ
# for godan verbs, but there the ō/ū is a real chōonpu, not the verb
# ending -- reverting it would turn "ikō" into the wrong "ikou".
_FINAL_OR_ATTRIBUTIVE_FORM_PREFIXES = ("終止形", "連体形")


class LongVowelResolver:
    """v1 handles exactly one closed-form case: a godan (五段) verb's
    dictionary/attributive form (終止形/連体形) always ends in kana う, which
    KanaRomanizer's default same-vowel/ou->ō contraction can mistake for a
    chōonpu (食う -> kū instead of kuu; 問う -> tō instead of tou). The 意志
    推量形 (volitional) form is excluded even though it also ends in ウ for
    godan verbs (行こう "ikō" is a genuine chōonpu, not the verb's own う).

    Any other uncertain long-vowel case -- notably compound-noun lexical
    boundaries like こおどり (小躍り) -- has no dedicated rule here and is
    left exactly as KanaRomanizer produced it (kōdori, not koodori). This
    is a known v1 gap, not an application of kana_romanizer_spec.md §44:
    §44 actually recommends the opposite (preserve the explicit "oo"
    rather than the collapsed "ō" when uncertain), which would require
    reverting KanaRomanizer's default here rather than leaving it --
    detecting that this specific token needs that treatment is exactly
    the compound-boundary information this resolver does not have.
    """

    def resolve(
        self, *, token: Token, kana_romanization: KanaRomanization
    ) -> KanaRomanization:
        if not _is_godan_verb_final_u(token):
            return kana_romanization

        final_vowel = kana_romanization.final_vowel
        if final_vowel is None or final_vowel not in MACRON_TO_VOWEL:
            return kana_romanization

        base_vowel = MACRON_TO_VOWEL[final_vowel]
        reverted_text = kana_romanization.text[:-1] + base_vowel + "u"

        return replace(kana_romanization, text=reverted_text, final_vowel="u")


def _is_godan_verb_final_u(token: Token) -> bool:
    return (
        token.conjugation_type is not None
        and token.conjugation_type.startswith(_GODAN_PREFIX)
        and token.conjugation_form is not None
        and token.conjugation_form.startswith(_FINAL_OR_ATTRIBUTIVE_FORM_PREFIXES)
        and token.kana is not None
        and token.kana.endswith(_VERB_FINAL_U_KANA)
    )
