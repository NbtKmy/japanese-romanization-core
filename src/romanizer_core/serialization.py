from .models.analysis import AnalysisResult, AnalyzerInfo
from .models.romanization_result import RomanizationResult
from .models.token import Token


def _analyzer_to_dict(analyzer: AnalyzerInfo) -> dict[str, object]:
    return {
        "name": analyzer.name,
        "version": analyzer.version,
        "dictionary": {
            "name": analyzer.dictionary.name,
            "version": analyzer.dictionary.version,
            "schema_id": analyzer.dictionary.schema_id,
        },
    }


def _token_to_dict(token: Token) -> dict[str, object]:
    return {
        "id": token.id,
        "surface": token.surface,
        "start": token.start,
        "end": token.end,
        "is_unknown": token.is_unknown,
        "lemma": token.lemma,
        "lemma_reading": token.lemma_reading,
        "pos": list(token.pos),
        "conjugation_type": token.conjugation_type,
        "conjugation_form": token.conjugation_form,
        "orth": token.orth,
        "kana": token.kana,
        "pronunciation": token.pronunciation,
        "form": token.form,
        "form_base": token.form_base,
        "word_type": token.word_type,
    }


def analysis_to_dict(result: AnalysisResult) -> dict[str, object]:
    """Convert an ``AnalysisResult`` to a plain, JSON-serializable dict matching the package's documented JSON shape."""
    return {
        "text": result.text,
        "analyzer": _analyzer_to_dict(result.analyzer),
        "tokens": [_token_to_dict(token) for token in result.tokens],
    }


def romanization_to_dict(result: RomanizationResult) -> dict[str, object]:
    """Convert a ``RomanizationResult`` to a plain, JSON-serializable dict.

    Each token dict gets a nested ``"romanization"`` entry, matched by
    ``Token.id`` against ``RomanizedToken.token_id`` (never by positional
    zip, so a misaligned result raises ``KeyError`` instead of silently
    producing wrong data). See
    docs/superpowers/specs/2026-09-26-phase4-public-api-design.md §5 for the
    full shape and the ``json_schema_version`` versioning rationale.
    """
    romanized_by_id = {rt.token_id: rt for rt in result.romanized_tokens}

    return {
        "json_schema_version": "1",
        "text": result.text,
        "romanized_text": result.romanized_text,
        "romanization_scheme": {
            "name": result.romanization_scheme.name,
            "version": result.romanization_scheme.version,
        },
        "analyzer": _analyzer_to_dict(result.analyzer),
        "tokens": [
            {
                **_token_to_dict(token),
                "romanization": {
                    "romaji": romanized_by_id[token.id].romaji,
                    "source": romanized_by_id[token.id].source,
                    "fuses_with_next": romanized_by_id[token.id].fuses_with_next,
                },
            }
            for token in result.tokens
        ],
    }
