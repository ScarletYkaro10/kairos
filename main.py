"""Ponto de entrada principal da aplicacao Kairos."""

from __future__ import annotations

import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent
src_dir = root_dir / "src"

for path in (root_dir, src_dir):
    str_path = str(path)
    if str_path not in sys.path:
        sys.path.insert(0, str_path)

from src.main import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
