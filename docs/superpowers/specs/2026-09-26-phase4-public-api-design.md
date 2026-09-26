# Phase 4: Public API / JSON Schema Stabilization — Design

## 1. 目的・背景

Phase 1–3で形態素解析(`MeCabAnalyzer`)、kana→romaji変換(`KanaRomanizer`)、token-level pipeline
(`ContextResolver`/`LongVowelResolver`/`TokenRomanizer`/`Renderer`)が完成した。

`romanizer-core_plan.md`の元マイルストーン(§21)ではこの次を「Phase 3: Additional Schemes
(Kunrei/Nihon)」としていたが、実装順は変更し、訓令式・日本式などの追加ローマ字方式は**別途後日**
実装する。今回のPhase 4は元マイルストーンの「Phase 4: Integration readiness」
(README整備・公開API最終整理・JSON schema安定化・MCP/App向けexample)に相当する。

**このPhaseのゴール:** 現在バラバラなクラス(`MeCabAnalyzer`/`TokenRomanizer`/`Renderer`)を1つの
公開APIにまとめ、JSON出力形を安定させ、README/exampleを整備する。将来 Kunrei/Nihon 等の
方式が追加されても、この外側のAPI/JSON形は壊れない設計にする。

## 2. スコープ判断（対話で確定した前提）

- **scheme対応の深さ:** 今回は外側API/JSON形の拡張性確保のみ。`KanaRomanizer`内部の
  長音マクロン処理・撥音アポストロフィ規則・促音tch規則、および`ContextResolver`/
  `LongVowelResolver`の判定ロジックはModified Hepburn固定のまま**リファクタしない**。
  訓令式実装着手時に内部設計を再検討する。
- **公開APIの形:** 単一`Romanizer`facadeクラスを新設。既存3クラスは内部実装として残す。
- **JSON形:** 各token dictに`"romanization"`入れ子を追加する方式（`romanizer-core_plan.md`
  §13の元案）。`tokens[]`と`romanized_tokens[]`を別配列で並べる方式は採らない。
- **JSONバージョニング:** 新設する`romanization_to_dict()`の出力にのみ`json_schema_version`
  フィールドを追加。既存`analysis_to_dict()`(Phase 1出力)の形は変更しない(後方互換)。
- **方式差の将来対応:** ALA-LC式など分かち書き規則が異なるローマ字方式が将来追加された場合も、
  `RomanizationScheme.name`で区別する。Rendererの空白規則自体をscheme-parameterized化するかは
  訓令式/ALA-LC式着手時に再検討する(今回は対応しない)。
- **JSON schemaの形式:** Pythonのdict shape + `json_schema_version`文字列のみ。
  json-schema.org形式の別ファイル(`.schema.json`)は今回作らない。
- **MCP/App向けexample:** README内のコードブロックのみ。`examples/`配下の実行可能scriptは作らない。

## 3. 新規モデル

### 3.1 `RomanizationScheme`

```python
# src/romanizer_core/models/romanization_scheme.py
@dataclass(frozen=True, slots=True)
class RomanizationScheme:
    name: str
    version: str
```

`kana/scheme.py`の`KanaSchemeDefinition`(マッピング表本体を保持する内部実装、`name`/`version`
フィールドも持つ)とは意図的に別の型とする。理由: `KanaSchemeDefinition`は`kana/`層の内部実装
詳細（辞書データそのもの）であり、将来訓令式追加時に内部表現が変わってもこの公開識別子は
不変でいられるようにするため。`Romanizer`facadeが内部で`KanaSchemeDefinition`から
`KanaRomanizer`を組み立てる一方、`RomanizationScheme`は公開結果(`RomanizationResult`)の
識別情報としてのみ使う。

v1では`MODIFIED_HEPBURN_V1`(`KanaSchemeDefinition`)と対応する
`RomanizationScheme(name="modified_hepburn", version="1")`を`Romanizer.modified_hepburn()`
factory内でハードコードする。両者の`name`/`version`文字列は一致させる(将来の混乱防止)。

### 3.2 `RomanizationResult`

```python
# src/romanizer_core/models/romanization_result.py
@dataclass(frozen=True, slots=True)
class RomanizationResult:
    text: str
    romanized_text: str
    romanization_scheme: RomanizationScheme
    analyzer: AnalyzerInfo
    tokens: tuple[Token, ...]
    romanized_tokens: tuple[RomanizedToken, ...]
```

`tokens`と`romanized_tokens`は同じ順序・同じ長さを保つ(`TokenRomanizer.romanize()`の既存
contractそのまま)。`RomanizedToken.token_id`は各`tokens[i].id`と一致する。

## 4. `Romanizer` facade

```python
# src/romanizer_core/romanizer.py
class Romanizer:
    def __init__(
        self,
        analyzer: MeCabAnalyzer,
        token_romanizer: TokenRomanizer,
        renderer: Renderer,
        scheme: RomanizationScheme,
    ) -> None: ...

    @classmethod
    def modified_hepburn(cls, analyzer: MeCabAnalyzer) -> "Romanizer":
        """MODIFIED_HEPBURN_V1を使うpipeline一式を組み立てる便利factory。"""
        ...

    def romanize(self, text: str) -> RomanizationResult:
        """MeCabAnalyzer.analyze() -> TokenRomanizer.romanize() -> Renderer.render()
        を順に呼び、1つのRomanizationResultにまとめる。"""
        ...
```

`romanize()`の内部フロー:

```text
text
  |
  v
MeCabAnalyzer.analyze(text)          -> AnalysisResult
  |
  v
TokenRomanizer.romanize(tokens)      -> tuple[RomanizedToken, ...]
  |
  v
Renderer.render(tokens, romanized_tokens) -> str (romanized_text)
  |
  v
RomanizationResult(...)
```

将来訓令式を実装する際は、並列する`Romanizer.kunrei_shiki(analyzer)`factoryを追加するだけで
済む想定(内部で別の`KanaSchemeDefinition`/`ContextResolver`/`LongVowelResolver`実装を
組み立てて`RomanizationScheme(name="kunrei_shiki", version="1")`を渡す)。

## 5. JSON出力

既存`analysis_to_dict()`(Phase 1、`AnalysisResult`用)は無変更。新設`romanization_to_dict()`
を`serialization.py`に追加する。

```python
def romanization_to_dict(result: RomanizationResult) -> dict[str, object]:
    ...
```

出力shape:

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

`tokens[i].romanization`は該当`Token.id`と一致する`RomanizedToken.token_id`を辞書引きして
組み立てる(位置zipではなくid参照)。ズレがあれば`KeyError`で即座に検知できる
(位置zipでの黙ったズレを防ぐ)。

`json_schema_version`はこの新shapeのみに付与する文字列フィールド。将来訓令式等が追加されて
このdict shape自体が変わる場合に備えたバージョン番号(現在`"1"`)。既存`analysis_to_dict()`
出力には付与しない(既存契約を変えない)。

## 6. 公開API (`__init__.py`)

追加export:

```python
"Romanizer",
"RomanizationResult",
"RomanizationScheme",
"romanization_to_dict",
```

既存exportは変更なし。

## 7. README再構成

現行`README.md`はCutlet謝辞1行のみ。以下の構成に全面書き直し:

1. タイトル・一行説明
2. Install (`uv add` / `uv sync`)
3. UniDic辞書セットアップ (`analyzer_interfaces.md`の`DictionaryConfig`節へリンク、辞書DL/配置は
   本パッケージの責務外である旨を明記)
4. Quick start (`Romanizer.modified_hepburn()` → `romanize()` → `.romanized_text`)
5. JSON出力サンプル (`romanization_to_dict()`の出力例、§5のJSON例を再掲)
6. 対応ローマ字方式 (現状: Modified Hepburn v1のみ。訓令式・日本式は今後追加予定と明記)
7. アーキテクチャ概要 (3行程度の概要 + `romanizer-core_plan.md`/`kana_romanizer_spec.md`への
   リンク。詳細をREADMEに複製しない)
8. 既存の謝辞(Cutlet)を維持

## 8. 変更ファイル一覧

- 新規: `src/romanizer_core/models/romanization_scheme.py`
- 新規: `src/romanizer_core/models/romanization_result.py`
- 新規: `src/romanizer_core/romanizer.py`
- 変更: `src/romanizer_core/serialization.py` (`romanization_to_dict`追加)
- 変更: `src/romanizer_core/__init__.py` (新規export追加)
- 変更: `README.md` (全面書き直し)
- 新規テスト: `tests/test_romanization_scheme.py`
- 新規テスト: `tests/test_romanization_result.py`
- 新規テスト: `tests/test_romanizer_facade.py` (実UniDic辞書使用、既存`dictionary_path`
  フィクスチャ流用。`Romanizer.modified_hepburn(analyzer).romanize(text)`が既存
  `TokenRomanizer`/`Renderer`のテストで確認済みの結果と一致することを確認)
- 新規テスト: `tests/test_serialization_romanization.py` (`romanization_to_dict`の形・
  `json_schema_version`・`romanization`入れ子・token_id対応付けを確認)
- 変更: `tests/test_package_api.py` (新規export importテスト追加)

## 9. スコープ外(今回やらないこと)

- 訓令式・日本式ローマ字方式の実装
- `KanaRomanizer`/`ContextResolver`/`LongVowelResolver`のscheme-parameterized化
- Rendererの分かち書き規則をscheme依存にする対応
- json-schema.org形式の`.schema.json`ファイル
- `examples/`配下の実行可能scriptファイル
- MCP/App側の実装(別リポジトリの責務)
