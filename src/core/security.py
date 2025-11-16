from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from ..models import schemas  # Importa o schema que acabamos de criar

# ==================================
#         Configuração de Hashing
# ==================================

# 1. Configurar o "CryptContext" do Passlib
# Estamos dizendo ao passlib para usar "bcrypt" como o algoritmo padrão
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar se a senha pura bate com o hash salvo
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o hash de uma senha pura
def get_password_hash(password: str) -> str:
    # Bcrypt tem um limite de 72 bytes. Vamos truncar a senha para evitar erros.
    password_bytes = password.encode('utf-8')
    truncated_bytes = password_bytes[:72]
    return pwd_context.hash(truncated_bytes)


# ==================================
#         Configuração de Token JWT
# ==================================

# !! IMPORTANTE !!
# Estas chaves devem vir de variáveis de ambiente no mundo real.
# Para o projeto, vamos deixá-las aqui por simplicidade.
# Esta é a sua "chave secreta" para assinar os tokens.
SECRET_KEY = "sua-chave-secreta-muito-forte-aqui" # Mude isso para qualquer frase
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Define que o token de login expira em 30 minutos

# Função para criar um novo token de acesso (JWT)
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    
    # Define o tempo de expiração do token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # "Assina" o token com nossos dados e a chave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar e decodificar um token
def verify_token(token: str, credentials_exception) -> schemas.TokenData:
    try:
        # Tenta decodificar o token usando nossa chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str | None = payload.get("sub")
        if email is None:
            # Se não houver "subject" (email), o token é inválido
            raise credentials_exception
        
        # Retorna os dados do token (o email do usuário)
        return schemas.TokenData(email=email)
    except JWTError:
        # Se o token estiver expirado ou a assinatura for inválida
        raise credentials_exception