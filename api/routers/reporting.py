from __future__ import annotations
from fastapi import APIRouter
from api.models import Report
from agents import data_quality, product, financial
from validation.validator import validate_report

router = APIRouter(prefix="/api", tags=["reporting"])

@router.get("/run", response_model=Report)
def run_agents() -> Report:
    insights, hypos = [], []
    for mod in (data_quality, product, financial):
        i, h = mod.run()
        insights.extend(i)
        hypos.extend(h)
    report = Report(
        id="rep-1",
        executive_summary="Automated weekly report (demo).",
        insights=insights,
        hypotheses=hypos,
        appendix=""
    )
    score = validate_report(report.model_dump())
    report.validator_scorecard = score
    return report
