from __future__ import annotations

import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def chatgpt_db(tmp_path_factory) -> str:
    """Provide a temporary copy of the repository's chatgpt.db for tests.

    Returns the filesystem path to the copied database so tests can connect
    without depending on CWD or mutating the source DB.
    """
    repo_root = Path(__file__).resolve().parents[1]
    src = repo_root / "chatgpt.db"
    if not src.exists():
        raise FileNotFoundError(f"Expected database not found: {src}")

    tmp_dir = tmp_path_factory.mktemp("chatgpt_db")
    dst = tmp_dir / "chatgpt.db"
    shutil.copyfile(src, dst)
    return str(dst)

