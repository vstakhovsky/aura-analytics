from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze", tags=["analyze"])
async def analyze_stub():
    """
    Возвращаем минимальный, но стабильный для тестов payload.
    """
    return {
        "status": "ok",
        "metrics": [
            {"key": "AS", "name": "Active Sessions", "value": 123, "unit": "count"},
            {"key": "CR", "name": "Conversion Rate", "value": 0.42, "unit": "ratio"}
        ]
    }
