from fastapi import HTTPException, status
from ..models import schemas
from ..core import security

# ==================================
#         Banco de Dados Falso
# ==================================

# Para o MVP de 50%, vamos usar um dicionário (Tabela de Hash) como
# um banco de dados em memória.
# Isso nos permite ter um pilar de segurança 100% funcional e testável
# sem a complexidade de um banco de dados real ainda.
# A chave será o email do usuário.
fake_users_db = {}

# ==================================
#         Lógica de Negócio (Serviços)
# ==================================

def register_user(user: schemas.UserCreate) -> schemas.UserPublic:
    """
    1. Verifica se o usuário já existe.
    2. Cria o hash da senha.
    3. Salva o novo usuário no "banco".
    4. Retorna o usuário público (sem a senha).
    """
    
    # 1. Verifica se o usuário já existe
    if user.email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado."
        )
        
    # 2. Cria o hash da senha (usando nossa função do security.py)
    hashed_password = security.get_password_hash(user.password)
    
    # 3. Salva o novo usuário
    # No mundo real, o ID seria gerado pelo banco (ex: MongoDB)
    user_id = str(len(fake_users_db) + 1) 
    
    fake_user_data = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password 
    }
    fake_users_db[user.email] = fake_user_data
    
    # 4. Retorna o usuário público (sem a senha)
    return schemas.UserPublic(id=user_id, email=user.email)


def login_user(form_data: schemas.UserCreate) -> schemas.Token:
    """
    1. Busca o usuário no "banco" pelo email.
    2. Verifica se a senha está correta.
    3. Cria e retorna um token JWT.
    """
    
    # 1. Busca o usuário
    user_in_db = fake_users_db.get(form_data.email)
    
    # Validação de usuário e senha
    if not user_in_db:
        # Usuário não encontrado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 2. Verifica a senha (usando nossa função do security.py)
    if not security.verify_password(form_data.password, user_in_db["hashed_password"]):
        # Senha incorreta
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Cria o token de acesso
    # O "subject" (sub) do token será o email do usuário
    access_token = security.create_access_token(
        data={"sub": user_in_db["email"]}
    )
    
    return schemas.Token(access_token=access_token, token_type="bearer")