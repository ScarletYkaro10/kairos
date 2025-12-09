from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import schemas
from ..models.database import User
from ..core import security


def _normalize_email(email: str) -> str:
    """Padroniza o email para minúsculas e remove espaços."""
    return email.lower().strip()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Busca um usuário no banco pelo email."""
    normalized_email = _normalize_email(email)
    return db.query(User).filter(User.email == normalized_email).first()


def register_user(user: schemas.UserCreate, db: Session) -> schemas.UserPublic:
    """Registra um novo usuário com senha hash."""
    normalized_email = _normalize_email(user.email)

    existing_user = get_user_by_email(db, normalized_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado."
        )

    hashed_password = security.get_password_hash(user.password)

    db_user = User(email=normalized_email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schemas.UserPublic(id=db_user.id, email=db_user.email)


def login_user(form_data: schemas.UserCreate, db: Session) -> schemas.Token:
    """Autentica o usuário e retorna o token JWT."""
    normalized_email = _normalize_email(form_data.email)
    user_in_db = get_user_by_email(db, normalized_email)

    dummy_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWrn3ILAWO.PzH12n.M9/1CV.b6M.u"

    hashed_password_to_check = user_in_db.hashed_password if user_in_db else dummy_hash

    if not security.verify_password(form_data.password, hashed_password_to_check):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(data={"sub": user_in_db.email})
    return schemas.Token(access_token=access_token, token_type="bearer")
