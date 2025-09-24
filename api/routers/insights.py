from fastapi import APIRouter

router = APIRouter()

@router.get("/insights", tags=["insights"])
def get_insights():
    """
    Минимальный ответ, достаточный для тестов/демо.
    Возвращаем статус и пару фиктивных инсайтов.
    """
    return {
        "status": "ok",
        "insights": [
            {"id": "i1", "title": "Retention dips on weekends", "impact": "medium"},
            {"id": "i2", "title": "AS churn correlates with failed payments", "impact": "high"},
        ],
        "count": 2,
    }
