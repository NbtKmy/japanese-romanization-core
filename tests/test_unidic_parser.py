import pytest

from romanizer_core.analyzer.schema import UNIDIC_CWJ_202512_SCHEMA
from romanizer_core.analyzer.unidic import RawToken, UniDicParser
from romanizer_core.exceptions import InvalidUnknownFeatureError, UnsupportedUniDicSchemaError

WAGAHAI_FEATURE = (
    "代名詞,*,*,*,*,*,ワガハイ,我が輩,吾輩,ワガハイ,吾輩,ワガハイ,混,*,*,*,*,*,*,"
    "体,ワガハイ,ワガハイ,ワガハイ,ワガハイ,0,*,*,11321954766299648,41189"
)
HA_FEATURE = (
    '助詞,係助詞,*,*,*,*,ハ,は,は,ワ,は,ワ,和,*,*,*,*,*,*,係助,ハ,ハ,ハ,ハ,*,'
    '"動詞%F2@0,名詞%F1,形容詞%F2@-1",*,8059703733133824,29321'
)
NEKO_FEATURE = (
    "名詞,普通名詞,一般,*,*,*,ネコ,猫,猫,ネコ,猫,ネコ,和,*,*,*,*,*,*,"
    "体,ネコ,ネコ,ネコ,ネコ,1,C4,*,7918141678166528,28806"
)
PYTHON_UNKNOWN_FEATURE = "名詞,普通名詞,一般,*,*,*"


@pytest.fixture
def parser() -> UniDicParser:
    return UniDicParser(UNIDIC_CWJ_202512_SCHEMA)


def test_parse_known_maps_basic_fields(parser):
    raw = RawToken(id="t0", surface="吾輩", start=0, end=2, is_unknown=False, feature=WAGAHAI_FEATURE)

    token = parser.parse_known(raw)

    assert token.id == "t0"
    assert token.surface == "吾輩"
    assert token.is_unknown is False
    assert token.lemma == "我が輩"
    assert token.lemma_reading == "ワガハイ"
    assert token.pos == ("代名詞",)
    assert token.conjugation_type is None
    assert token.conjugation_form is None
    assert token.orth == "吾輩"
    assert token.kana == "ワガハイ"
    assert token.pronunciation == "ワガハイ"
    assert token.form == "ワガハイ"
    assert token.form_base == "ワガハイ"
    assert token.word_type == "混"


def test_parse_known_normalizes_multi_level_pos(parser):
    raw = RawToken(id="t0", surface="猫", start=0, end=1, is_unknown=False, feature=NEKO_FEATURE)

    token = parser.parse_known(raw)

    assert token.pos == ("名詞", "普通名詞", "一般")


def test_parse_known_distinguishes_kana_from_pronunciation(parser):
    raw = RawToken(id="t1", surface="は", start=2, end=3, is_unknown=False, feature=HA_FEATURE)

    token = parser.parse_known(raw)

    assert token.kana == "ハ"
    assert token.pronunciation == "ワ"
    assert token.kana != token.pronunciation


def test_parse_known_handles_quoted_csv_field_with_embedded_commas(parser):
    raw = RawToken(id="t1", surface="は", start=2, end=3, is_unknown=False, feature=HA_FEATURE)

    token = parser.parse_known(raw)

    assert token.pos == ("助詞", "係助詞")


def test_parse_known_raises_on_field_count_mismatch(parser):
    truncated_feature = ",".join(WAGAHAI_FEATURE.split(",")[:-1])
    raw = RawToken(id="t0", surface="吾輩", start=0, end=2, is_unknown=False, feature=truncated_feature)

    with pytest.raises(UnsupportedUniDicSchemaError) as exc_info:
        parser.parse_known(raw)

    assert exc_info.value.expected == 29
    assert exc_info.value.actual == 28


def test_parse_unknown_sets_is_unknown_and_nulls_lexical_fields(parser):
    raw = RawToken(id="t2", surface="Python", start=0, end=6, is_unknown=True, feature=PYTHON_UNKNOWN_FEATURE)

    token = parser.parse_unknown(raw)

    assert token.is_unknown is True
    assert token.pos == ("名詞", "普通名詞", "一般")
    assert token.lemma is None
    assert token.lemma_reading is None
    assert token.kana is None
    assert token.pronunciation is None
    assert token.orth is None
    assert token.form is None
    assert token.form_base is None
    assert token.word_type is None


def test_parse_unknown_raises_when_feature_too_short(parser):
    raw = RawToken(id="t2", surface="Python", start=0, end=6, is_unknown=True, feature="名詞,普通名詞")

    with pytest.raises(InvalidUnknownFeatureError) as exc_info:
        parser.parse_unknown(raw)

    assert exc_info.value.expected_at_least == 6
    assert exc_info.value.actual == 2


def test_parse_dispatches_to_known_or_unknown(parser):
    known_raw = RawToken(id="t0", surface="猫", start=0, end=1, is_unknown=False, feature=NEKO_FEATURE)
    unknown_raw = RawToken(id="t1", surface="Python", start=2, end=8, is_unknown=True, feature=PYTHON_UNKNOWN_FEATURE)

    assert parser.parse(known_raw).is_unknown is False
    assert parser.parse(unknown_raw).is_unknown is True
