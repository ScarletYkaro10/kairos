from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer  
from src.core import security
from src.models import schemas
from src.services import auth_service

security_scheme = HTTPBearer()

def get_current_user_id(token_auth=Depends(security_scheme)) -> str:
    """
    Dependência de porteiro (Atualizada para HTTPBearer).
    1. Pega o token do objeto de autorização.
    2. Verifica validade.
    3. Retorna o ID.
    """
    token = token_auth.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = security.verify_token(token, credentials_exception)

    user_in_db = auth_service.fake_users_db.get(token_data.email)

    if user_in_db is None:
        raise credentials_exception

    return user_in_db["id"]
