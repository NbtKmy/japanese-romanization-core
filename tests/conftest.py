from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DICTIONARY_PATH = PROJECT_ROOT / "unidic-cwj-202512"


@pytest.fixture(scope="session")
def dictionary_path() -> Path:
    if not DICTIONARY_PATH.exists():
        pytest.skip(f"UniDic dictionary not found at {DICTIONARY_PATH}")
    return DICTIONARY_PATH
