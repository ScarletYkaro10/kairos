from fastapi import FastAPI
from .api import auth_router  # Importa o router que acabamos de criar

# Cria a instância principal da aplicação
app = FastAPI(
    title="Kairós API",
    description="API do projeto Kairós - Assistente de Produtividade com IA",
    version="0.1.0"
)

# "Pluga" o router de autenticação na aplicação principal
app.include_router(auth_router.router)

# Um endpoint "raiz" só para sabermos que a API está no ar
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à Kairós API"}