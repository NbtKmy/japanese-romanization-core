def test_package_is_importable():
    import romanizer_core  # noqa: F401


def test_dictionary_fixture_resolves(dictionary_path):
    assert (dictionary_path / "dicrc").exists()
    assert (dictionary_path / "sys.dic").exists()


def test_end_to_end_analysis_via_public_api(dictionary_path):
    from romanizer_core import (
        AnalysisResult,
        DictionaryConfig,
        MeCabAnalyzer,
        MeCabAnalyzerConfig,
        Token,
        analysis_to_dict,
    )

    config = MeCabAnalyzerConfig(
        dictionary=DictionaryConfig(path=dictionary_path, version="202512"),
    )
    analyzer = MeCabAnalyzer(config)

    result = analyzer.analyze("吾輩は猫である")

    assert isinstance(result, AnalysisResult)
    assert all(isinstance(t, Token) for t in result.tokens)

    data = analysis_to_dict(result)
    assert data["text"] == "吾輩は猫である"
    assert data["tokens"][0]["surface"] == "吾輩"
