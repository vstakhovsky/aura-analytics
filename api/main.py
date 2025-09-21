from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api.routers.reporting import router as reporting_router
from api.routers.health import router as health_router
from api.routers.upload import router as upload_router
from api.routers.health import router as health_router
from api.routers.upload import router as upload_router

app = FastAPI(title="Aura Analytics Demo")

# API routers
app.include_router(reporting_router)
app.include_router(health_router)   # /health
app.include_router(upload_router)   # /upload/ , /ingest/{upload_id}  # /api/run (существующий)
app.include_router(health_router)     # /health
app.include_router(upload_router)     # /upload/ , /ingest/{upload_id}

# Минимальный UI (если был)
UI_DIR = Path(__file__).resolve().parents[1] / "ui"
if UI_DIR.exists():
    app.mount("/", StaticFiles(directory=UI_DIR, html=True), name="ui")
