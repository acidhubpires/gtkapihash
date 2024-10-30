from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Tuple
import os
import json
import glob  # Adiciona esta linha para importar o glob
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Diretórios para uploads e rastreamento
UPLOAD_FOLDER = 'upload'
TRACKING_FOLDER = 'app/uploads/tracking'

# Criação dos diretórios para uploads e rastreamento, caso não existam
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRACKING_FOLDER, exist_ok=True)

# Modelo para JSON de rastreamento em tempo real
class RealTimeData(BaseModel):
    username: str
    timestamp: str
    user_position: Tuple[float, float]
    erbs: List[dict]

# Rota para monitoramento em tempo real (recebe JSON)
@router.post("/track")
async def track_user(data: RealTimeData):
    try:
        tracking_data = {
            "username": data.username,  # Certifique-se de incluir o username
            "timestamp": data.timestamp,
            "user_position": data.user_position,
            "erbs": data.erbs
        }

        # Salva os dados no arquivo específico do usuário
        user_file = os.path.join(TRACKING_FOLDER, f"{data.username}_track.json")
        if os.path.exists(user_file):
            with open(user_file, "r+") as f:
                user_history = json.load(f)
                user_history.append(tracking_data)
                f.seek(0)
                json.dump(user_history, f, indent=2)
        else:
            with open(user_file, "w") as f:
                json.dump([tracking_data], f, indent=2)

        return {"status": "success", "message": f"Dados de {data.username} recebidos com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados: {str(e)}")

# Rota para upload de arquivos
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_location, "wb") as f:
            f.write(await file.read())

        return {"status": "success", "message": f"Arquivo {file.filename} recebido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")

# Rota para retornar dados de rastreamento
@router.get("/tracking-data")
async def get_tracking_data():
    try:
        tracking_files = glob.glob(f"{TRACKING_FOLDER}/*_track.json")
        all_data = []

        for file in tracking_files:
            with open(file, 'r') as f:
                user_data = json.load(f)
                all_data.extend(user_data)

        return all_data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao decodificar JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados de rastreamento: {str(e)}")

# Rota para a página de monitoramento
@router.get("/monitor", response_class=HTMLResponse)
async def monitor_page(request: Request):
    return templates.TemplateResponse("monitor.html", {"request": request})
