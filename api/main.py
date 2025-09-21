from fastapi import FastAPI

from api.routers.reporting import router as reporting_router
from api.routers.health import router as health_router
from api.routers.upload import router as upload_router

app = FastAPI(title="Aura Analytics Demo")

# Основной роутер с /api/run  и т.п.
app.include_router(reporting_router)
# Здоровье сервиса
app.include_router(health_router)   # /health
# Загрузка/инжест
app.include_router(upload_router)   # /upload/  и  /ingest/{upload_id}
