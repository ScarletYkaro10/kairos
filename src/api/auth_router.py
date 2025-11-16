from fastapi import APIRouter, status
from ..models import schemas
from ..services import auth_service

# Criamos um "router", que é como um mini-app FastAPI
router = APIRouter(
    prefix="/auth",         # Todas as rotas aqui começarão com /auth
    tags=["Autenticação"]   # Agrupa no /docs do Swagger
)

@router.post(
    "/register",
    response_model=schemas.UserPublic,    # Resposta segura (sem a senha)
    status_code=status.HTTP_201_CREATED # Status 201 para "Criado"
)
async def register(user_data: schemas.UserCreate):
    """
    Endpoint para registrar um novo usuário.
    Os dados (user_data) são validados pelo schema UserCreate.
    """
    # A mágica da Arquitetura Limpa:
    # O router não tem lógica, ele só chama o serviço.
    # O FastAPI vai capturar o HTTPException do serviço automaticamente.
    return auth_service.register_user(user=user_data)


@router.post("/login", response_model=schemas.Token)
async def login(login_data: schemas.UserCreate):
    """
    Endpoint para logar um usuário.
    Reutilizamos o schema UserCreate por simplicidade do MVP.
    """
    # O serviço faz toda a validação e retorna o token
    return auth_service.login_user(form_data=login_data)