from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Token:
    id: str

    # Original input
    surface: str
    start: int
    end: int
    is_unknown: bool

    # Lexical information
    lemma: str | None
    lemma_reading: str | None

    # Morphology
    pos: tuple[str, ...]
    conjugation_type: str | None
    conjugation_form: str | None

    # UniDic surface/form information
    orth: str | None
    kana: str | None
    pronunciation: str | None
    form: str | None
    form_base: str | None

    # Lexical origin
    word_type: str | None
