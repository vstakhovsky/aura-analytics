# health.py — trivial readiness endpoint
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
