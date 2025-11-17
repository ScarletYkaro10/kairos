from __future__ import annotations

import sys
from pathlib import Path

# Adiciona o diretorio raiz ao PYTHONPATH para permitir imports de src
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

