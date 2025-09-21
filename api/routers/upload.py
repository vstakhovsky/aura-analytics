from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

@router.get("/upload/", tags=["upload"])
def upload_root():
    # для контракта/тестов достаточно присутствия в OpenAPI и статус: ok
    return {"status": "ok"}

@router.post("/ingest/{upload_id}", tags=["upload"])
async def ingest_stub(upload_id: str):
    """
    Заглушка ingestion: создаёт data/uploads/<upload_id>/ и кладёт маркер _INGEST_OK.
    Тело не требуется; возвращает 200 и {"status":"ok"}.
    """
    base = Path(__file__).resolve().parents[2] / "data" / "uploads" / upload_id
    base.mkdir(parents=True, exist_ok=True)
    (base / "_INGEST_OK").write_text("ok")
    return {"upload_id": upload_id, "status": "ok"}
