from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
def health():
    # Тест ждёт status == "ok"
    return {"status": "ok"}
