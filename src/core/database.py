from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL do banco de dados - usa variável de ambiente ou padrão para SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./kairos.db"  # Padrão para desenvolvimento local
)

# Para PostgreSQL, a URL seria: postgresql://user:password@host:port/dbname
# Exemplo: postgresql://kairos:kairos123@db:5432/kairos

# Se a URL começar com postgresql://, converte para postgresql+psycopg2
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False,  # Mude para True para ver queries SQL no console
)

# SessionLocal para criar sessões de banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


def get_db():
    """
    Dependency para obter uma sessão do banco de dados.
    Usado com FastAPI Depends().
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Cria todas as tabelas no banco de dados.
    Deve ser chamado na inicialização da aplicação.
    """
    Base.metadata.create_all(bind=engine)

