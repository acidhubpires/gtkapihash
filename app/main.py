# Caminho: app/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.route import router  # Importa o router definido em route.py
from fastapi.staticfiles import StaticFiles
import os


# Instancia o aplicativo FastAPI
app = FastAPI()

# Montar a pasta 'asset' para servir arquivos estáticos
asset_path = os.path.join("app", "templates", "asset")
app.mount("/asset", StaticFiles(directory=asset_path), name="asset")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" permite todas as origens; substitua por uma lista de URLs específicas para maior segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o router do arquivo route.py
app.include_router(router)

# Rota de exemplo na raiz para verificar se o aplicativo está ativo
@app.get("/")
async def root():
    return {"message": "API está ativa e funcionando!"}
