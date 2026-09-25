import os
from pathlib import Path

import MeCab

from ..exceptions import (
    AnalyzerConfigurationError,
    DictionaryNotFoundError,
    InvalidDictionaryError,
    MeCabInitializationError,
)
from ..models.analysis import AnalyzerInfo, DictionaryInfo
from .config import MeCabAnalyzerConfig
from .schema import get_schema
from .unidic import UniDicParser


def _validate_dictionary_path(path: Path) -> None:
    if not path.exists():
        raise DictionaryNotFoundError(path)
    if not path.is_dir():
        raise InvalidDictionaryError(path)


class MeCabAnalyzer:
    def __init__(
        self,
        config: MeCabAnalyzerConfig,
        parser: UniDicParser | None = None,
    ) -> None:
        self._config = config

        schema = get_schema(config.dictionary.schema_id)

        if parser is not None and parser.schema.id != schema.id:
            raise AnalyzerConfigurationError(
                "Parser schema and dictionary schema do not match: "
                f"parser={parser.schema.id!r} dictionary={schema.id!r}"
            )

        self._parser = parser or UniDicParser(schema)

        if config.validate_dictionary:
            _validate_dictionary_path(config.dictionary.path)

        self._tagger = self._create_tagger(config.dictionary.path)
        self._info = self._build_analyzer_info()

    def _create_tagger(self, dictionary_path: Path) -> MeCab.Tagger:
        args = f'-r {os.devnull} -d "{dictionary_path}"'
        try:
            return MeCab.Tagger(args)
        except RuntimeError as exc:
            raise MeCabInitializationError(
                f"Failed to initialize MeCab with dictionary {dictionary_path}"
            ) from exc

    def _build_analyzer_info(self) -> AnalyzerInfo:
        return AnalyzerInfo(
            name="mecab",
            version=self._tagger.version(),
            dictionary=DictionaryInfo(
                name=self._config.dictionary.name,
                version=self._config.dictionary.version,
                schema_id=self._config.dictionary.schema_id,
            ),
        )

    @property
    def info(self) -> AnalyzerInfo:
        return self._info
