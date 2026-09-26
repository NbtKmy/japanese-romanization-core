"""Joins RomanizedToken output into one romanized_text string
(kana_romanizer_spec.md Part XIII / romanizer-core_plan.md §14).
"""

from typing import Sequence

from ..models.romanized_token import RomanizedToken
from ..models.token import Token

_SYMBOL_POS = "補助記号"
_OPEN_BRACKET_POS2 = "括弧開"


class Renderer:
    """Token-boundary spacing rules:

    - no space is inserted where TokenRomanizer reported
      ``fuses_with_next`` (a resolved cross-token っ/ん fusion);
    - no space before a UniDic 補助記号 (auxiliary symbol) token other than
      an opening bracket, and no space after an opening bracket;
    - the first character of the final string is capitalized.
    """

    def render(
        self, tokens: Sequence[Token], romanized_tokens: Sequence[RomanizedToken]
    ) -> str:
        parts: list[str] = []
        suppress_space_before_next = False

        for token, rtoken in zip(tokens, romanized_tokens, strict=True):
            romaji = rtoken.romaji
            if romaji == "":
                suppress_space_before_next = False
                continue

            is_opening_punctuation = _is_symbol(token) and _is_open_bracket(token)
            is_closing_punctuation = _is_symbol(token) and not is_opening_punctuation

            if parts and not suppress_space_before_next and not is_closing_punctuation:
                parts.append(" ")
            parts.append(romaji)

            suppress_space_before_next = rtoken.fuses_with_next or is_opening_punctuation

        text = "".join(parts)
        return _capitalize_first_letter(text)


def _is_symbol(token: Token) -> bool:
    return bool(token.pos) and token.pos[0] == _SYMBOL_POS


def _is_open_bracket(token: Token) -> bool:
    return len(token.pos) > 1 and token.pos[1] == _OPEN_BRACKET_POS2


def _capitalize_first_letter(text: str) -> str:
    for i, char in enumerate(text):
        if char.isalpha():
            return text[:i] + char.upper() + text[i + 1 :]
    return text
