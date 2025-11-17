from fastapi import HTTPException, status
from ..models import schemas
from ..core import security

fake_users_db = {}

def register_user(user: schemas.UserCreate) -> schemas.UserPublic:
    """
    1. Verifica se o usuário já existe.
    2. Cria o hash da senha.
    3. Salva o novo usuário no "banco".
    4. Retorna o usuário público (sem a senha).
    """
    
    if user.email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado."
        )
        
    hashed_password = security.get_password_hash(user.password)
    
    user_id = str(len(fake_users_db) + 1) 
    
    fake_user_data = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password 
    }
    fake_users_db[user.email] = fake_user_data
    
    return schemas.UserPublic(id=user_id, email=user.email)


def login_user(form_data: schemas.UserCreate) -> schemas.Token:
    """
    1. Busca o usuário no "banco" pelo email.
    2. Verifica se a senha está correta.
    3. Cria e retorna um token JWT.
    """
    
    user_in_db = fake_users_db.get(form_data.email)
    

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not security.verify_password(form_data.password, user_in_db["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = security.create_access_token(
        data={"sub": user_in_db["email"]}
    )
    
    return schemas.Token(access_token=access_token, token_type="bearer")