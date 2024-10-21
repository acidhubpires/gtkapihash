from fastapi import FastAPI
from app.api.route import router

app = FastAPI()

# Incluindo as rotas
app.include_router(router)
