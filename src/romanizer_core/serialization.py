from .models.analysis import AnalysisResult
from .models.token import Token


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
        "analyzer": {
            "name": result.analyzer.name,
            "version": result.analyzer.version,
            "dictionary": {
                "name": result.analyzer.dictionary.name,
                "version": result.analyzer.dictionary.version,
                "schema_id": result.analyzer.dictionary.schema_id,
            },
        },
        "tokens": [_token_to_dict(token) for token in result.tokens],
    }
