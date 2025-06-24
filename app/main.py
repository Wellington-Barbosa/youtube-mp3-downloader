from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
from pathlib import Path
from tkinter import Tk, filedialog
from fastapi.responses import JSONResponse
import sys
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Verifica se está rodando como executável PyInstaller
if getattr(sys, 'frozen', False):
    # Caminho dentro do executável
    ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg', 'bin')
else:
    # Caminho normal em modo dev
    ffmpeg_path = './ffmpeg/bin'

user_download_path = None

def escolher_pasta():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tk
    folder_selected = filedialog.askdirectory(title="Selecione a pasta para salvar o download")
    return folder_selected

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/download")
async def api_download_audio(youtube_url: str = Form(...), download_path: str = Form(None)):
    global user_download_path

    try:
        if not download_path and not user_download_path:
            download_path = escolher_pasta()
            user_download_path = download_path
        elif not download_path and user_download_path:
            download_path = user_download_path
        else:
            user_download_path = download_path

        target_path = Path(download_path)
        target_path.mkdir(parents=True, exist_ok=True)

        output_template = str(target_path / "%(title)s.%(ext)s")

        command = [
            "yt-dlp",
            "--no-playlist",
            "-x",
            "--audio-format", "mp3",
            "--ffmpeg-location", ffmpeg_path,
            "-o", output_template,
            youtube_url
        ]

        subprocess.run(command, check=True)
        return JSONResponse({"status": "success", "message": f"✅ Download concluído! Arquivo salvo em: {target_path}"})

    except Exception as e:
        return JSONResponse({"status": "error", "message": f"❌ Erro no download: {str(e)}"})