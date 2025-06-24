from pathlib import Path

# Caminho padrão para salvar os MP3
DOWNLOAD_PATH = Path(__file__).resolve().parent.parent / "downloads"
DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
