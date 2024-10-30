from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.services.file_processing import processar_arquivo_upload  # Certifique-se de que este caminho esteja correto
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Criação do diretório para uploads, caso não exista
UPLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Rota para a página inicial (se houver frontend, pode ser usada para testar)
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para o formulário de upload (frontend opcional para testes com navegadores)
@router.get("/upload", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# Rota para processar o upload do arquivo
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Salvar o arquivo enviado temporariamente na pasta de uploads
        file_location = f"{UPLOAD_FOLDER}/{file.filename}"

        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Processa o arquivo enviado e retorna um GeoDataFrame ou coordenadas processadas
        resultados = processar_arquivo_upload(file_location)

        # Extrair as coordenadas e nomenclaturas geradas para retorno
        coordenadas = []
        nomenclaturas = []
        for resultado in resultados:
            coordenadas.append(resultado['coordenada'])
            nomenclaturas.append(resultado['nomenclatura'])

        # Retorna o JSON com as coordenadas e nomenclaturas geradas
        return {
            "coordenadas": coordenadas,
            "nomenclaturas": nomenclaturas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")
    finally:
        # Remover o arquivo temporário após o processamento
        if os.path.exists(file_location):
            os.remove(file_location)
