"""
Script para criar as tabelas no banco de dados.
Execute: python scripts/create_tables.py
"""
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.core.database import init_db
from src.models import database  

if __name__ == "__main__":
    print("Criando tabelas no banco de dados...")
    try:
        init_db()
        print("✅ Tabelas criadas com sucesso!")
        print("Tabelas criadas:")
        print("  - users")
        print("  - tasks")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        sys.exit(1)

