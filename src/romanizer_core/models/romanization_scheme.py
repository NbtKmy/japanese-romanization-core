from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RomanizationScheme:
    """Public identifier for a romanization scheme (e.g. "modified_hepburn"
    version "1"). Deliberately separate from ``kana.scheme.KanaSchemeDefinition``,
    which holds that scheme's actual mapping-table data as an internal
    implementation detail of the ``kana`` layer -- this type is what
    ``RomanizationResult`` and its JSON serialization expose publicly, and it
    stays stable even if the internal mapping representation changes.
    """

    name: str
    version: str
