from pathlib import Path
from fastapi import APIRouter

router = APIRouter(tags=["upload"])

@router.get("/upload/")
def upload_root():
    # наличие в OpenAPI достаточно для теста
    return {"ok": True}

@router.post("/ingest/{upload_id}")
async def ingest_stub(upload_id: str):
    """
    Stub ingest: создаёт data/uploads/<upload_id>/ и кладёт маркер _INGEST_OK.
    Тела запроса не требуется; возвращаем 200.
    """
    base = Path(__file__).resolve().parents[2] / "data" / "uploads" / upload_id
    base.mkdir(parents=True, exist_ok=True)
    (base / "_INGEST_OK").write_text("ok")
    return {"upload_id": upload_id, "status": "saved"}
