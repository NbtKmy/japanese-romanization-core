import os
import shlex
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


def build_mecab_args(*, rc_path: str, dictionary_path: Path) -> str:
    """Build the MeCab option string for ``MeCab.Tagger``.

    Both ``rc_path`` and ``dictionary_path`` are individually shell-quoted
    with ``shlex.quote`` before being joined, so this is safe for paths
    containing spaces, double quotes, or other shell-special characters
    (mecab-python3 parses the resulting string with ``shlex.split``).
    """
    return f"-r {shlex.quote(rc_path)} -d {shlex.quote(str(dictionary_path))}"


class MeCabAnalyzer:
    """Wraps a MeCab tagger bound to a specific UniDic dictionary.

    An instance is NOT thread-safe: create one analyzer per worker/thread
    rather than sharing an instance across threads. Construction validates
    the configured dictionary path and initializes the underlying MeCab
    tagger eagerly, so a misconfigured dictionary fails fast at
    construction time rather than on the first call to :meth:`analyze`.
    """

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
        args = build_mecab_args(rc_path=os.devnull, dictionary_path=dictionary_path)
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
        """Read-only info about this analyzer and its dictionary."""
        return self._info

    def analyze(self, text: str) -> AnalysisResult:
        """Analyze ``text`` into a tuple of :class:`Token`\\ s.

        For every returned token, the span invariant
        ``text[token.start:token.end] == token.surface`` holds; ``start``
        and ``end`` are Python Unicode code-point indices into ``text``
        (not MeCab byte offsets). An empty string input returns an
        ``AnalysisResult`` with no tokens without raising. Text containing
        a NUL character (``"\\x00"``) raises :class:`AnalysisError`, since
        MeCab's underlying C-string layer would otherwise silently
        truncate the input at the NUL.
        """
        if not isinstance(text, str):
            raise TypeError("text must be str")

        if "\x00" in text:
            raise AnalysisError("text must not contain NUL characters")

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
