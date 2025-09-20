from __future__ import annotations
from typing import List, Dict, Optional
from pydantic import BaseModel


class Metric(BaseModel):
    name: str
    value: float | int | str | None = None
    unit: Optional[str] = None
    method: Optional[str] = None


class Figure(BaseModel):
    caption: str
    path: str  # relative asset path, e.g. "figs/chart.png"


class Insight(BaseModel):
    id: str
    domain: str
    title: str
    summary: str
    confidence: float
    impact: str
    metrics: List[Metric] = []
    figures: List[Figure] = []
    methodology: Optional[str] = None
    evidence: Optional[str] = None  # pointer to SQL/nb/md


class Complexity(BaseModel):
    dev_weeks: int


class Hypothesis(BaseModel):
    id: str
    title: str
    problem: str
    domain: str
    metrics: List[Dict] = []
    complexity: Complexity
    summary: str


class Report(BaseModel):
    id: str
    executive_summary: str
    insights: List[Insight]
    hypotheses: List[Hypothesis]
    appendix: str = ""
    validator_scorecard: Dict = {}
