from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RomanizedToken:
    """One token's contribution to the rendered romanization.

    ``source`` records which Token field produced ``romaji``: ``"kana"``,
    ``"pronunciation"``, ``"orth"``, or ``"surface"`` (kana_romanizer_spec.md
    Part XIII / romanizer-core_plan.md §18). ``fuses_with_next`` is set by
    TokenRomanizer when a trailing sokuon/moraic-n was phonetically resolved
    against the next token (kana_romanizer_spec.md Part VI/VII); Renderer
    must not insert a space at that boundary.
    """

    token_id: str
    romaji: str
    source: str
    fuses_with_next: bool = False
