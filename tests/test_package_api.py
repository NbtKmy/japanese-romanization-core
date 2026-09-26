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


def test_phase3_pipeline_types_are_importable_from_root():
    from romanizer_core import (
        ContextResolver,
        LongVowelResolver,
        Renderer,
        RomanizedToken,
        TokenRomanizer,
    )

    assert ContextResolver is not None
    assert LongVowelResolver is not None
    assert Renderer is not None
    assert RomanizedToken is not None
    assert TokenRomanizer is not None


def test_phase4_public_api_types_are_importable_from_root():
    from romanizer_core import (
        RomanizationResult,
        RomanizationScheme,
        Romanizer,
        romanization_to_dict,
    )

    assert RomanizationResult is not None
    assert RomanizationScheme is not None
    assert Romanizer is not None
    assert romanization_to_dict is not None


def test_romanizer_end_to_end_via_public_api(dictionary_path):
    from romanizer_core import (
        DictionaryConfig,
        MeCabAnalyzer,
        MeCabAnalyzerConfig,
        Romanizer,
        romanization_to_dict,
    )

    analyzer = MeCabAnalyzer(
        MeCabAnalyzerConfig(
            dictionary=DictionaryConfig(path=dictionary_path, version="202512")
        )
    )
    romanizer = Romanizer.modified_hepburn(analyzer)

    result = romanizer.romanize("吾輩は猫である。")
    data = romanization_to_dict(result)

    assert result.romanized_text == "Wagahai wa neko de aru。"
    assert data["romanized_text"] == "Wagahai wa neko de aru。"
    assert data["json_schema_version"] == "1"
