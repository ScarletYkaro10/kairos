from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import schemas
from ..models.database import User
from ..core import security


def _normalize_email(email: str) -> str:
    """Normaliza o email para lowercase (emails são case-insensitive)."""
    return email.lower().strip()


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Busca um usuário pelo email no banco de dados.
    """
    normalized_email = _normalize_email(email)
    return db.query(User).filter(User.email == normalized_email).first()


def register_user(user: schemas.UserCreate, db: Session) -> schemas.UserPublic:
    """
    1. Verifica se o usuário já existe.
    2. Cria o hash da senha.
    3. Salva o novo usuário no banco de dados.
    4. Retorna o usuário público (sem a senha).
    """
    normalized_email = _normalize_email(user.email)

    # Verifica se o usuário já existe
    existing_user = get_user_by_email(db, normalized_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado."
        )

    # Cria hash da senha
    hashed_password = security.get_password_hash(user.password)

    # Cria novo usuário
    db_user = User(
        email=normalized_email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schemas.UserPublic(id=db_user.id, email=db_user.email)


def login_user(form_data: schemas.UserCreate, db: Session) -> schemas.Token:
    """
    1. Busca o usuário no banco de dados pelo email.
    2. Verifica se a senha está correta.
    3. Cria e retorna um token JWT.

    Nota: Sempre verifica a senha para evitar timing attacks que possam
    vazar informações sobre quais emails existem no sistema.
    """
    normalized_email = _normalize_email(form_data.email)
    user_in_db = get_user_by_email(db, normalized_email)

    # Hash dummy para manter tempo de resposta similar (mitiga timing attack)
    dummy_hash = "$2b$12$dummy.hash.to.prevent.timing.attack.here"
    hashed_password_to_check = user_in_db.hashed_password if user_in_db else dummy_hash

    # Sempre verifica a senha, mesmo se o usuário não existir
    if not security.verify_password(form_data.password, hashed_password_to_check):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Se chegou aqui, a senha está correta, mas verifica se o usuário existe
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(data={"sub": user_in_db.email})

    return schemas.Token(access_token=access_token, token_type="bearer")
