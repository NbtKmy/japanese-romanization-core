"""Public facade: MeCabAnalyzer -> TokenRomanizer -> Renderer, in one call
(romanizer-core_plan.md §14, docs/superpowers/specs/2026-09-26-phase4-public-api-design.md §4).
"""

from .analyzer.mecab import MeCabAnalyzer
from .kana.romanizer import KanaRomanizer
from .kana.scheme import MODIFIED_HEPBURN_V1
from .models.romanization_result import RomanizationResult
from .models.romanization_scheme import RomanizationScheme
from .romanization.context_resolver import ContextResolver
from .romanization.long_vowel_resolver import LongVowelResolver
from .romanization.renderer import Renderer
from .romanization.token_romanizer import TokenRomanizer


class Romanizer:
    def __init__(
        self,
        analyzer: MeCabAnalyzer,
        token_romanizer: TokenRomanizer,
        renderer: Renderer,
        scheme: RomanizationScheme,
    ) -> None:
        self._analyzer = analyzer
        self._token_romanizer = token_romanizer
        self._renderer = renderer
        self._scheme = scheme

    @classmethod
    def modified_hepburn(cls, analyzer: MeCabAnalyzer) -> "Romanizer":
        """Build a ``Romanizer`` wired for the Modified Hepburn v1 scheme."""
        return cls(
            analyzer=analyzer,
            token_romanizer=TokenRomanizer(
                kana_romanizer=KanaRomanizer(MODIFIED_HEPBURN_V1),
                context_resolver=ContextResolver(),
                long_vowel_resolver=LongVowelResolver(),
            ),
            renderer=Renderer(),
            # Hardcoded, not derived from MODIFIED_HEPBURN_V1.name/.version:
            # this public identifier must stay stable even if the internal
            # KanaSchemeDefinition's own name/version ever change (spec §3.1).
            scheme=RomanizationScheme(name="modified_hepburn", version="1"),
        )

    def romanize(self, text: str) -> RomanizationResult:
        analysis = self._analyzer.analyze(text)
        romanized_tokens = self._token_romanizer.romanize(analysis.tokens)
        romanized_text = self._renderer.render(analysis.tokens, romanized_tokens)

        return RomanizationResult(
            text=analysis.text,
            romanized_text=romanized_text,
            romanization_scheme=self._scheme,
            analyzer=analysis.analyzer,
            tokens=analysis.tokens,
            romanized_tokens=romanized_tokens,
        )
