from typing import Mapping


def longest_match(
    text: str, index: int, lookup: Mapping[str, str]
) -> tuple[str, str] | None:
    """Find the longest mapped kana substring at ``text[index:]``.

    Tries 3-, then 2-, then 1-character candidates against ``lookup`` and
    returns the first hit as ``(source, romaji)``, or ``None`` if nothing
    matches.
    """

    for length in (3, 2, 1):
        candidate = text[index : index + length]
        if len(candidate) == length and candidate in lookup:
            return candidate, lookup[candidate]

    return None
