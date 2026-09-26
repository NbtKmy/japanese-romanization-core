from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KanaRomanization:
    """The result of romanizing one kana string with KanaRomanizer.

    ``text`` is a token-level romanization candidate, not necessarily the
    final output for a whole utterance. ``pending_sokuon``/
    ``pending_syllabic_n`` signal that a trailing ``っ``/``ん`` could not be
    resolved without seeing the next token (left to a future
    ContextResolver); ``final_vowel`` exposes the trailing vowel of the
    generated sequence for a future LongVowelResolver to inspect.
    """

    text: str
    pending_sokuon: bool = False
    pending_syllabic_n: bool = False
    final_vowel: str | None = None
