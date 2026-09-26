"""Corrects lexical/morphological long-vowel exceptions that KanaRomanizer's
kana-local default cannot know about (kana_romanizer_spec.md §43/§44).
"""

from dataclasses import replace

from ..kana.macron import MACRON_TO_VOWEL
from ..models.kana_romanization import KanaRomanization
from ..models.token import Token

_GODAN_PREFIX = "五段"
_VERB_FINAL_U_KANA = ("う", "ウ")


class LongVowelResolver:
    """v1 handles exactly one closed-form case: a godan (五段) verb's
    dictionary/attributive form always ends in kana う, which
    KanaRomanizer's default same-vowel/ou->ō contraction can mistake for a
    chōonpu (食う -> kū instead of kuu; 問う -> tō instead of tou). Any other
    uncertain long-vowel case (e.g. compound-noun lexical boundaries like
    こおどり) is left unchanged: preserving the kana-local default is safer
    than guessing (kana_romanizer_spec.md §44).
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
        and token.kana is not None
        and token.kana.endswith(_VERB_FINAL_U_KANA)
    )
