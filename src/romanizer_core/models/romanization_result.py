from dataclasses import dataclass

from .analysis import AnalyzerInfo
from .romanization_scheme import RomanizationScheme
from .romanized_token import RomanizedToken
from .token import Token


@dataclass(frozen=True, slots=True)
class RomanizationResult:
    """The full result of romanizing one piece of text: the original
    analysis (``analyzer``, ``tokens``) plus the romanization pipeline's
    output (``romanized_text``, ``romanized_tokens``) and which scheme
    produced it.

    ``tokens`` and ``romanized_tokens`` are the same length and order
    (``romanized_tokens[i].token_id == tokens[i].id`` for every ``i``),
    per ``TokenRomanizer.romanize()``'s existing contract.
    """

    text: str
    romanized_text: str
    romanization_scheme: RomanizationScheme
    analyzer: AnalyzerInfo
    tokens: tuple[Token, ...]
    romanized_tokens: tuple[RomanizedToken, ...]
