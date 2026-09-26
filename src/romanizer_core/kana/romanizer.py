from types import MappingProxyType
from typing import Mapping

from ..models.kana_romanization import KanaRomanization
from .iteration import resolve_iteration_mark
from .macron import MACRON
from .prepare import prepare_kana
from .scanner import longest_match
from .scheme import KanaSchemeDefinition

_VOWELS = {"a", "i", "u", "e", "o"}

_LONE_VOWEL_KANA = {"あ": "a", "い": "i", "う": "u", "え": "e", "お": "o"}


def sokuon_prefix(next_romaji: str) -> str:
    if next_romaji.startswith("ch"):
        return "t"
    return next_romaji[:1]


class KanaRomanizer:
    """Token-free, low-level kana-to-romaji converter for one KanaSchemeDefinition."""

    def __init__(self, definition: KanaSchemeDefinition) -> None:
        self._definition = definition
        self._lookup: Mapping[str, str] = MappingProxyType(
            {
                **definition.base_mapping,
                **definition.modern_extensions,
                **definition.rare_extensions,
            }
        )

    def romanize(self, kana: str) -> KanaRomanization:
        if not isinstance(kana, str):
            raise TypeError("kana must be str")

        prepared = prepare_kana(kana)
        lookup = self._lookup

        out: list[str] = []
        last_vowel: str | None = None
        last_mora_kana: str | None = None
        pending_sokuon = False
        pending_syllabic_n = False

        i = 0
        n = len(prepared)

        while i < n:
            char = prepared[i]

            if char in ("ゝ", "ヽ", "ゞ", "ヾ"):
                resolved = resolve_iteration_mark(
                    mark=char, last_mora_kana=last_mora_kana, lookup=lookup
                )
                if resolved is None:
                    out.append(char)
                    last_vowel = None
                    last_mora_kana = None
                else:
                    mora_kana, romaji = resolved
                    out.append(romaji)
                    last_vowel = romaji[-1] if romaji[-1] in _VOWELS else None
                    last_mora_kana = mora_kana
                i += 1
                continue

            if char == "ん":
                lookahead = longest_match(prepared, i + 1, lookup)
                if lookahead is None:
                    if i + 1 >= n:
                        # Token-final ん: whether it stays "n" or becomes
                        # "n'" depends on the next token's initial sound,
                        # which KanaRomanizer cannot see (spec §38).
                        pending_syllabic_n = True
                    out.append("n")
                else:
                    _, next_romaji = lookahead
                    if next_romaji[:1] in _VOWELS or next_romaji.startswith("y"):
                        out.append("n'")
                    else:
                        out.append("n")
                last_vowel = None
                last_mora_kana = "ん"
                i += 1
                continue

            if char == "ー":
                if last_vowel is not None and last_vowel in MACRON and out:
                    macron = MACRON[last_vowel]
                    out[-1] = out[-1][:-1] + macron
                    last_vowel = macron
                else:
                    # Nothing to lengthen (start of string, or the
                    # preceding mora didn't end in a plain vowel):
                    # preserve rather than crash (spec §47/§48).
                    out.append("ー")
                    last_vowel = None
                last_mora_kana = None
                i += 1
                continue

            if char == "っ":
                lookahead = longest_match(prepared, i + 1, lookup)
                if lookahead is None:
                    # End of input, or the following text isn't a mapped
                    # mora at all (e.g. a token boundary, or genuinely
                    # unmappable text). Either way we defer rather than
                    # guess; KanaRomanizer itself never emits the "'"
                    # abrupt-cutoff spelling from spec §35 — that belongs
                    # to whatever resolves pending_sokuon downstream.
                    pending_sokuon = True
                else:
                    _, next_romaji = lookahead
                    out.append(sokuon_prefix(next_romaji))
                    # Do not consume the following mora here; let the next
                    # loop iteration process it through the normal path so
                    # its romaji/last_vowel bookkeeping happens exactly once.
                last_mora_kana = None
                i += 1
                continue

            match = longest_match(prepared, i, lookup)

            if match is None:
                out.append(char)
                last_vowel = None
                last_mora_kana = None
                i += 1
                continue

            source, romaji = match

            # Default same-vowel / historical ou->ō contraction (spec
            # Part VIII §41/§56). This only fires for a lone vowel kana
            # character immediately following a matching vowel, never for
            # an arbitrary consonant-mora that happens to share a vowel
            # sound (e.g. とと stays "toto", not "tō"). "い" is excluded so
            # both "ii" and "ei" are always retained per spec; lexical
            # exceptions to this default (くう->kuu, こおどり->koodori) are
            # LongVowelResolver's responsibility, out of scope here.
            if (
                source in _LONE_VOWEL_KANA
                and source != "い"
                and last_vowel is not None
                and out
            ):
                vowel = _LONE_VOWEL_KANA[source]
                if last_vowel == vowel or (last_vowel == "o" and source == "う"):
                    macron = MACRON[last_vowel]
                    out[-1] = out[-1][:-1] + macron
                    last_vowel = macron
                    last_mora_kana = source
                    i += len(source)
                    continue

            out.append(romaji)
            last_vowel = romaji[-1] if romaji[-1] in _VOWELS else None
            last_mora_kana = source
            i += len(source)

        return KanaRomanization(
            text="".join(out),
            pending_sokuon=pending_sokuon,
            pending_syllabic_n=pending_syllabic_n,
            final_vowel=last_vowel,
        )
