from __future__ import annotations

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import pandas as pd
import io
import os
from typing import Any, Dict, List

app = FastAPI(title="AURA Analytics API", version="0.1.0")

# --- In-memory хранилище данных для MVP ---
DATAFRAME: pd.DataFrame | None = None
LAST_INGEST_INFO: Dict[str, Any] = {}

# ---- Модели ответов (MVP-уровня) ----
class Metric(BaseModel):
    key: str
    value: Any
    description: str
    computed: bool

class Insight(BaseModel):
    id: str
    title: str
    hypothesis: str
    problem: str
    impact: str
    stakeholders: List[str]
    domain: str
    data_fields: List[str]
    confidence: float  # 0..1
    metrics: List[str]
    complexity: str
    risks: List[str]
    priority: str
    summary: str
    teams: List[str]
    consequence_if_ignored: str
    comments: str = ""

# ---- Служебное ----
def _read_any_to_df(upload: UploadFile) -> pd.DataFrame:
    name = (upload.filename or "").lower()
    raw = upload.file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty file")

    # CSV / JSON
    try:
        if name.endswith(".csv"):
            return pd.read_csv(io.BytesIO(raw))
        if name.endswith(".json"):
            return pd.read_json(io.BytesIO(raw))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse {name}: {e}")

    # Fallback: попробуем угадать CSV
    try:
        return pd.read_csv(io.BytesIO(raw))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unsupported format for {name}: {e}")

def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # Нормализация типичных полей (мягко, чтобы не падать)
    lower_cols = {c: c.strip().lower() for c in df.columns}
    df = df.rename(columns=lower_cols)

    # Парсим таймштампы, если есть
    for cand in ["started_at", "start_time", "timestamp", "ts", "date"]:
        if cand in df.columns:
            df[cand] = pd.to_datetime(df[cand], errors="coerce")
            break

    # Булевы поля мягко приводим
    for cand in ["ai_used", "cws", "provisioned"]:
        if cand in df.columns:
            df[cand] = df[cand].astype(str).str.lower().isin(["1", "true", "yes", "y", "t"])

    # Длительность мин (если есть)
    if "duration_min" in df.columns:
        df["duration_min"] = pd.to_numeric(df["duration_min"], errors="coerce")

    return df

def _compute_metrics(df: pd.DataFrame) -> List[Metric]:
    metrics: List[Metric] = []
    cols = set(df.columns)

    # Active Seats (AS) = уникальные пользователи по user_id
    if "user_id" in cols:
        as_val = int(df["user_id"].nunique())
        metrics.append(Metric(key="AS", value=as_val, description="Active seats (unique users)", computed=True))
    else:
        metrics.append(Metric(key="AS", value=None, description="Active seats (unique users)", computed=False))

    # Adoption Rate (ARp) — доля пользователей с >= N сессий (прокси)
    if "user_id" in cols:
        sessions_per_user = df.groupby("user_id").size()
        arp = float((sessions_per_user >= 3).mean())  # доля «устойчиво активных»
        metrics.append(Metric(key="ARp", value=round(arp, 3), description="Adoption rate (proxy: users with ≥3 sessions)", computed=True))
    else:
        metrics.append(Metric(key="ARp", value=None, description="Adoption rate (proxy)", computed=False))

    # AI coverage (AIcov) — доля событий/сессий с ai_used=True
    if "ai_used" in cols:
        aicov = float(df["ai_used"].mean()) if len(df) else 0.0
        metrics.append(Metric(key="AIcov", value=round(aicov, 3), description="Share of sessions with AI usage", computed=True))
    else:
        metrics.append(Metric(key="AIcov", value=None, description="Share of sessions with AI usage", computed=False))

    # Code With Me Sessions (CWS) — количество сессий с cws=True
    if "cws" in cols:
        cws_count = int(df["cws"].sum())
        metrics.append(Metric(key="CWS", value=cws_count, description="Count of collaboration (Code With Me) sessions", computed=True))
    else:
        metrics.append(Metric(key="CWS", value=None, description="Count of collaboration sessions", computed=False))

    # Provisioning OK rate (ProvOK) — доля provisioned=True
    if "provisioned" in cols:
        prov_ok = float(df["provisioned"].mean()) if len(df) else 0.0
        metrics.append(Metric(key="ProvOK", value=round(prov_ok, 3), description="Provisioning success rate", computed=True))
    else:
        metrics.append(Metric(key="ProvOK", value=None, description="Provisioning success rate", computed=False))

    return metrics

def _derive_insights(df: pd.DataFrame, metrics: List[Metric]) -> List[Insight]:
    # Простые правила — безопасные, не зависят от конкретной схемы
    m = {x.key: x for x in metrics}
    insights: List[Insight] = []

    # 1) Низкое покрытие AI
    if m["AIcov"].computed and m["AIcov"].value is not None and m["AIcov"].value < 0.2:
        confidence = max(0.4, min(0.9, len(df)/1000.0))
        insights.append(Insight(
            id="ai-low-coverage",
            title="Low AI feature coverage",
            hypothesis="AI features are underused across teams",
            problem="Potential productivity uplift from AI assistance is not realized",
            impact="Reduced dev throughput; slower code reviews; longer time-to-ship",
            stakeholders=["DPE Manager", "Team Leads", "Developers"],
            domain="developer_productivity",
            data_fields=[c for c in df.columns if c in ["ai_used","user_id","started_at"]],
            confidence=round(confidence, 2),
            metrics=["AIcov","ARp"],
            complexity="Medium",
            risks=["Over-attributing value to AI", "Privacy concerns if tracking too granular"],
            priority="High",
            summary="AI usage < 20%; consider enablement, prompts, or policy to drive adoption.",
            teams=["Platform/DevEx","Security/Compliance (policy)"],
            consequence_if_ignored="AI ROI remains unrealized; org falls behind peers",
            comments=""
        ))

    # 2) Падает провиженинг
    if m["ProvOK"].computed and m["ProvOK"].value is not None and m["ProvOK"].value < 0.95:
        insights.append(Insight(
            id="provisioning-issues",
            title="Provisioning success below target",
            hypothesis="Provisioning errors block usage and adoption",
            problem="Users cannot start sessions reliably",
            impact="Lower adoption & satisfaction; more support load",
            stakeholders=["Platform Ops","IT"],
            domain="platform_reliability",
            data_fields=[c for c in df.columns if c in ["provisioned","user_id","started_at"]],
            confidence=0.7,
            metrics=["ProvOK","ARp"],
            complexity="Low",
            risks=["Misclassification of transient errors"],
            priority="High",
            summary="Provisioning success rate < 95%; investigate error sources and retry policies.",
            teams=["Platform Ops","SRE"],
            consequence_if_ignored="Adoption stalls; reputational risk",
            comments=""
        ))

    # 3) Мало коллаборации (CWS)
    if m["CWS"].computed and m["CWS"].value is not None and m["CWS"].value == 0:
        insights.append(Insight(
            id="collab-missing",
            title="Collaboration sessions not observed",
            hypothesis="Teams are not using collaboration features",
            problem="Missed opportunities for pair reviews/mentoring",
            impact="Slower onboarding; knowledge silos",
            stakeholders=["Team Leads","Developers"],
            domain="continuous_learning",
            data_fields=[c for c in df.columns if c in ["cws","user_id","started_at"]],
            confidence=0.6,
            metrics=["CWS","ARp"],
            complexity="Low",
            risks=["CWS not instrumented in dataset"],
            priority="Medium",
            summary="No collaboration sessions recorded; consider enablement and docs.",
            teams=["DevEx","Developer Education"],
            consequence_if_ignored="Slower ramp-up; lower code quality",
            comments=""
        ))

    return insights

def _metrics_to_md(metrics: List[Metric]) -> str:
    lines = ["## Metrics"]
    for m in metrics:
        status = "✅" if m.computed else "⚪"
        lines.append(f"- {status} **{m.key}**: {m.value} — _{m.description}_")
    return "\n".join(lines)

def _insights_to_md(insights: List[Insight]) -> str:
    if not insights:
        return "## Insights\n_No insights produced for current dataset._"
    out = ["## Insights"]
    for ins in insights:
        out.append(f"### {ins.title} ({ins.id})")
        out.append(f"- Hypothesis: {ins.hypothesis}")
        out.append(f"- Problem: {ins.problem}")
        out.append(f"- Impact: {ins.impact}")
        out.append(f"- Stakeholders: {', '.join(ins.stakeholders)}")
        out.append(f"- Domain: {ins.domain}")
        out.append(f"- Metrics: {', '.join(ins.metrics)}")
        out.append(f"- Confidence: {ins.confidence}")
        out.append(f"- Priority: {ins.priority} | Complexity: {ins.complexity}")
        out.append(f"- Summary: {ins.summary}")
        out.append(f"- Consequence if ignored: {ins.consequence_if_ignored}")
        out.append("")
    return "\n".join(out)

# ---- Эндпоинты ----
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    global DATAFRAME, LAST_INGEST_INFO
    df = _read_any_to_df(file)
    df = _normalize_df(df)
    DATAFRAME = df
    LAST_INGEST_INFO = {
        "rows": len(df),
        "cols": list(df.columns),
        "source": file.filename,
    }
    return {"status": "ok", "ingested": LAST_INGEST_INFO}

@app.post("/ingest/sample")
async def ingest_sample():
    """Удобно для демо: берет sample_data/ide_sessions.csv из репо."""
    global DATAFRAME, LAST_INGEST_INFO
    path = os.path.join(os.path.dirname(__file__), "..", "..", "sample_data", "ide_sessions.csv")
    path = os.path.normpath(path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="sample_data/ide_sessions.csv not found")
    df = pd.read_csv(path)
    df = _normalize_df(df)
    DATAFRAME = df
    LAST_INGEST_INFO = {"rows": len(df), "cols": list(df.columns), "source": "sample_data/ide_sessions.csv"}
    return {"status": "ok", "ingested": LAST_INGEST_INFO}

@app.post("/analyze")
async def analyze():
    if DATAFRAME is None or len(DATAFRAME) == 0:
        raise HTTPException(status_code=400, detail="No data ingested yet")
    metrics = _compute_metrics(DATAFRAME)
    return {"status": "ok", "metrics": [m.model_dump() for m in metrics], "ingest": LAST_INGEST_INFO}

@app.get("/insights")
async def insights():
    if DATAFRAME is None or len(DATAFRAME) == 0:
        raise HTTPException(status_code=400, detail="No data ingested yet")
    metrics = _compute_metrics(DATAFRAME)
    ins = _derive_insights(DATAFRAME, metrics)
    return {"status": "ok", "count": len(ins), "insights": [i.model_dump() for i in ins]}

@app.get("/report", response_class=PlainTextResponse)
async def report():
    if DATAFRAME is None or len(DATAFRAME) == 0:
        raise HTTPException(status_code=400, detail="No data ingested yet")
    metrics = _compute_metrics(DATAFRAME)
    ins = _derive_insights(DATAFRAME, metrics)
    md = ["# AURA Analytics — Report (MVP)", ""]
    md.append(_metrics_to_md(metrics))
    md.append("")
    md.append(_insights_to_md(ins))
    content = "\n".join(md)
    return content
