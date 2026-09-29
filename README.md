# japanese-romanization-core

日本語テキストを形態素解析し、ローマ字化するcoreライブラリ。MeCab + UniDicによる解析結果と、
そのローマ字化根拠（どのフィールドから生成したか）を構造化データとして返す。LLMは呼ばない
（意味論的な補正は利用側の責務）。

## Install

未PyPI公開のため、`uv add japanese-romanization-core` は使えない。以下のいずれかの方法を使う。

Gitリポジトリを直接指定する場合:

```bash
uv add git+https://github.com/NbtKmy/japanese-romanization-core.git
```

リポジトリをクローンして開発する場合:

```bash
git clone https://github.com/NbtKmy/japanese-romanization-core.git
cd japanese-romanization-core
uv sync
```

## UniDic辞書の準備

本パッケージはUniDic辞書のダウンロード・配置を行わない。国立国語研究所配布の
UniDic-CWJ辞書を別途用意し、`DictionaryConfig(path=..., name=..., version=...)` で
パスを明示的に渡す（下のQuick start参照）。

## Quick start

```python
from pathlib import Path
from romanizer_core import (
    DictionaryConfig,
    MeCabAnalyzer,
    MeCabAnalyzerConfig,
    Romanizer,
)

analyzer = MeCabAnalyzer(
    MeCabAnalyzerConfig(
        dictionary=DictionaryConfig(
            path=Path("unidic-cwj-202512"),
            version="202512",
        )
    )
)
romanizer = Romanizer.modified_hepburn(analyzer)

result = romanizer.romanize("吾輩は猫である。")
print(result.romanized_text)  # "Wagahai wa neko de aru。"
```

## JSON出力

```python
from romanizer_core import romanization_to_dict
import json

print(json.dumps(romanization_to_dict(result), ensure_ascii=False, indent=2))
```

```json
{
  "json_schema_version": "1",
  "text": "吾輩は猫である。",
  "romanized_text": "Wagahai wa neko de aru。",
  "romanization_scheme": {
    "name": "modified_hepburn",
    "version": "1"
  },
  "analyzer": {
    "name": "mecab",
    "version": "0.996",
    "dictionary": {
      "name": "unidic-cwj",
      "version": "202512",
      "schema_id": "unidic-cwj-202512-29"
    }
  },
  "tokens": [
    {
      "id": "t0",
      "surface": "吾輩",
      "start": 0,
      "end": 2,
      "is_unknown": false,
      "lemma": "我が輩",
      "lemma_reading": "ワガハイ",
      "pos": ["代名詞"],
      "conjugation_type": null,
      "conjugation_form": null,
      "orth": "吾輩",
      "kana": "ワガハイ",
      "pronunciation": "ワガハイ",
      "form": "ワガハイ",
      "form_base": "ワガハイ",
      "word_type": "混",
      "romanization": {
        "romaji": "wagahai",
        "source": "kana",
        "fuses_with_next": false
      }
    }
  ]
}
```

`json_schema_version` はこのJSON shape自体のバージョン。将来ローマ字方式が増えて
shapeが変わる場合に備えた識別子で、現在は `"1"`。

## 対応ローマ字方式

現在対応しているのは Modified Hepburn v1 (`Romanizer.modified_hepburn()`) のみ。
訓令式・日本式は今後追加予定 (`docs/superpowers/specs/2026-09-26-phase4-public-api-design.md`
参照)。

## アーキテクチャ概要

```text
text -> MeCabAnalyzer.analyze() -> AnalysisResult (Token[])
      -> TokenRomanizer.romanize() -> RomanizedToken[]
      -> Renderer.render() -> romanized_text
```

`Romanizer.romanize()` はこの3段を1回の呼び出しにまとめ、`RomanizationResult` を返す。
各層の詳細な契約は `src/romanizer_core/` 配下の各モジュールのdocstringを参照。
公開APIの設計判断は
`docs/superpowers/specs/2026-09-26-phase4-public-api-design.md` にまとめてある。

## Acknowledgements

The kana romanization implementation was informed in part by
Cutlet by Paul O'Leary McCann:
https://github.com/polm/cutlet
