from fastapi import APIRouter

router = APIRouter()

@router.get("/report", tags=["report"])
def get_report():
    """
    Minimal stub endpoint used by tests and CI.
    Returns status ok.
    """
    return {"status": "ok"}
