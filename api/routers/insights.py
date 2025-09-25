# api/routers/insights.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/insights", tags=["insights"])
def get_insights():
    """
    Minimal read-only Insights endpoint for tests/demo.
    Returns a basic payload with status and a couple of fake insights.
    """
    return {
        "status": "ok",
        "insights": [
            {"id": "i1", "title": "Retention dips on weekends", "impact": "medium"},
            {"id": "i2", "title": "AS churn correlates with failed payments", "impact": "high"},
        ],
        "count": 2,
    }
