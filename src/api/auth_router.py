from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..models import schemas
from ..services import auth_service
from ..core.database import get_db


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/register", response_model=schemas.UserPublic, status_code=status.HTTP_201_CREATED
)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar um novo usuário.
    Os dados (user_data) são validados pelo schema UserCreate.
    """
    return auth_service.register_user(user=user_data, db=db)


@router.post("/login", response_model=schemas.Token)
async def login(login_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para logar um usuário.
    Reutilizamos o schema UserCreate por simplicidade do MVP.
    """
    return auth_service.login_user(form_data=login_data, db=db)
