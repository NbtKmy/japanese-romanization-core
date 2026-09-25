import os
from pathlib import Path

import MeCab

from ..exceptions import (
    AnalysisError,
    AnalyzerConfigurationError,
    DictionaryNotFoundError,
    InvalidDictionaryError,
    MeCabInitializationError,
    RomanizerCoreError,
    SpanResolutionError,
)
from ..models.analysis import AnalysisResult, AnalyzerInfo, DictionaryInfo
from .config import MeCabAnalyzerConfig
from .schema import get_schema
from .unidic import RawToken, UniDicParser


def _validate_dictionary_path(path: Path) -> None:
    if not path.exists():
        raise DictionaryNotFoundError(path)
    if not path.is_dir():
        raise InvalidDictionaryError(path)


def _is_bos_or_eos(node: MeCab.Node) -> bool:
    return node.stat in (MeCab.MECAB_BOS_NODE, MeCab.MECAB_EOS_NODE)


def _is_unknown(node: MeCab.Node) -> bool:
    return node.stat == MeCab.MECAB_UNK_NODE


def _resolve_span(*, text: str, surface: str, cursor: int) -> tuple[int, int]:
    start = text.find(surface, cursor)
    if start < 0:
        raise SpanResolutionError(surface=surface, cursor=cursor)
    return start, start + len(surface)


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

    def analyze(self, text: str) -> AnalysisResult:
        if not isinstance(text, str):
            raise TypeError("text must be str")

        if text == "":
            return AnalysisResult(text=text, analyzer=self.info, tokens=())

        tokens = []
        cursor = 0

        try:
            node = self._tagger.parseToNode(text)

            while node is not None:
                if _is_bos_or_eos(node):
                    node = node.next
                    continue

                surface = node.surface
                start, end = _resolve_span(text=text, surface=surface, cursor=cursor)

                raw = RawToken(
                    id=f"t{len(tokens)}",
                    surface=surface,
                    start=start,
                    end=end,
                    is_unknown=_is_unknown(node),
                    feature=node.feature,
                )

                tokens.append(self._parser.parse(raw))
                cursor = end
                node = node.next

        except RomanizerCoreError:
            raise
        except Exception as exc:
            raise AnalysisError(f"Failed to analyze text: {text!r}") from exc

        return AnalysisResult(text=text, analyzer=self.info, tokens=tuple(tokens))
