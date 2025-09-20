from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from api.routers.reporting import router as reporting_router

app = FastAPI(title="Aura Analytics Demo")
app.include_router(reporting_router)

UI_DIR = Path(__file__).resolve().parents[1] / "ui"
app.mount("/", StaticFiles(directory=UI_DIR, html=True), name="ui")
