"""Joins RomanizedToken output into one romanized_text string
(kana_romanizer_spec.md Part XIII / romanizer-core_plan.md §14).
"""

from typing import Sequence

from ..models.romanized_token import RomanizedToken
from ..models.token import Token

_SYMBOL_POS = "補助記号"
_WHITESPACE_POS = "空白"
_OPEN_BRACKET_POS2 = "括弧開"
_SENTENCE_END_POS2 = "句点"


class Renderer:
    """Token-boundary spacing rules:

    - no space is inserted where TokenRomanizer reported
      ``fuses_with_next`` (a resolved cross-token っ/ん fusion);
    - no space before a UniDic 補助記号 (auxiliary symbol) token other than
      an opening bracket, and no space after an opening bracket;
    - a UniDic 空白 (whitespace) token contributes a single separator, not
      its literal (often full-width) character;
    - the first letter of each sentence is capitalized: the very start of
      the text, and again after each 句点-classified 補助記号 (。！？).
      A non-letter token (e.g. a leading number) occupies that position
      without being capitalized, and capitalization does not hunt past it
      into a later word.
    """

    def render(
        self, tokens: Sequence[Token], romanized_tokens: Sequence[RomanizedToken]
    ) -> str:
        parts: list[str] = []
        suppress_space_before_next = False
        capitalize_next = True

        for token, rtoken in zip(tokens, romanized_tokens, strict=True):
            romaji = rtoken.romaji
            if romaji == "" or _is_whitespace(token):
                suppress_space_before_next = False
                continue

            is_symbol_token = _is_symbol(token)
            is_opening_punctuation = is_symbol_token and _is_open_bracket(token)
            is_closing_punctuation = is_symbol_token and not is_opening_punctuation

            if parts and not suppress_space_before_next and not is_closing_punctuation:
                parts.append(" ")

            if not is_symbol_token:
                if capitalize_next:
                    romaji = _capitalize_first_letter(romaji)
                capitalize_next = False

            parts.append(romaji)

            suppress_space_before_next = rtoken.fuses_with_next or is_opening_punctuation
            if is_symbol_token and _is_sentence_end(token):
                capitalize_next = True

        return "".join(parts)


def _is_symbol(token: Token) -> bool:
    return bool(token.pos) and token.pos[0] == _SYMBOL_POS


def _is_whitespace(token: Token) -> bool:
    return bool(token.pos) and token.pos[0] == _WHITESPACE_POS


def _is_open_bracket(token: Token) -> bool:
    return len(token.pos) > 1 and token.pos[1] == _OPEN_BRACKET_POS2


def _is_sentence_end(token: Token) -> bool:
    return len(token.pos) > 1 and token.pos[1] == _SENTENCE_END_POS2


def _capitalize_first_letter(text: str) -> str:
    for i, char in enumerate(text):
        if char.isalpha():
            return text[:i] + char.upper() + text[i + 1 :]
    return text
