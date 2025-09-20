# upload.py — minimal upload/ingest surface for tests
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

@router.get("/upload/", tags=["upload"])
def upload_root():
    # Presence in OpenAPI is enough for the test
    return {"ok": True}

@router.post("/ingest/{upload_id}", tags=["upload"])
async def ingest_stub(upload_id: str):
    """
    Stub ingest: create data/uploads/<upload_id>/ and drop a marker file.
    No body is required for tests; returns 200 on success.
    """
    base = Path(__file__).resolve().parents[2] / "data" / "uploads" / upload_id
    base.mkdir(parents=True, exist_ok=True)
    (base / "_INGEST_OK").write_text("ok")
    return {"upload_id": upload_id, "status": "saved"}
