from pydantic import BaseModel, EmailStr, Field, ConfigDict

# ==================================
#         Schemas de Usuário
# ==================================

# Schema para validação de entrada na criação de usuário
# Isso garante que só receberemos um email válido e uma senha forte
class UserCreate(BaseModel):
    email: EmailStr  # Valida automaticamente se é um email
    password: str = Field(..., min_length=8) # Exige senha com no mínimo 8 caracteres

# Schema para o que vamos retornar ao público (NUNCA a senha)
class UserPublic(BaseModel):
    id: str  # Vamos usar um ID (ex: do MongoDB ou um UUID)
    email: EmailStr

    # Configuração para permitir que o Pydantic leia o modelo do banco
    model_config = ConfigDict(from_attributes=True)

# ==================================
#         Schemas de Token (Login)
# ==================================

# Schema para o que a API vai retornar após um login bem-sucedido
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema interno para carregar os dados do payload do JWT
class TokenData(BaseModel):
    email: str | None = None