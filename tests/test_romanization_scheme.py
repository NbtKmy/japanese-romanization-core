from romanizer_core.models.romanization_scheme import RomanizationScheme


def test_romanization_scheme_holds_name_and_version():
    scheme = RomanizationScheme(name="modified_hepburn", version="1")
    assert scheme.name == "modified_hepburn"
    assert scheme.version == "1"


def test_romanization_scheme_is_frozen():
    scheme = RomanizationScheme(name="modified_hepburn", version="1")
    try:
        scheme.name = "kunrei_shiki"  # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("expected AttributeError on mutation")
