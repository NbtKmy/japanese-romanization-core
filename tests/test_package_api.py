def test_package_is_importable():
    import romanizer_core  # noqa: F401


def test_dictionary_fixture_resolves(dictionary_path):
    assert (dictionary_path / "dicrc").exists()
    assert (dictionary_path / "sys.dic").exists()
