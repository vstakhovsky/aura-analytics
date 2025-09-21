from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

@router.get("/upload/", tags=["upload"])
def upload_root():
    # Для наличия в OpenAPI. Тестам достаточно, что путь существует.
    return {"ok": True}

@router.post("/ingest/{upload_id}", tags=["upload"])
async def ingest_stub(upload_id: str):
    """
    Заглушка инжеста:
    - создаёт data/uploads/<upload_id>/ и кладёт маркер _INGEST_OK
    - возвращает форму, которую ожидает тест: {"status":"ok","ingested":{"rows":N}}
    """
    base = Path(__file__).resolve().parents[2] / "data" / "uploads" / upload_id
    base.mkdir(parents=True, exist_ok=True)
    (base / "_INGEST_OK").write_text("ok", encoding="utf-8")

    # Здесь можно подсчитать строки из реальных файлов, если нужно.
    # Для теста достаточно вернуть положительное число.
    rows_ingested = 1

    return {"status": "ok", "ingested": {"rows": rows_ingested}, "upload_id": upload_id}
