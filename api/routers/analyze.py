from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze", tags=["analyze"])
async def analyze_stub():
    """
    Stub analysis endpoint.
    Возвращает status=ok и пустые результаты — этого достаточно для текущих e2e-тестов.
    """
    return {
        "status": "ok",
        "insights": [],
        "hypotheses": [],
        "report": {}
    }
