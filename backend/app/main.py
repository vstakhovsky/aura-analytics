from __future__ import annotations
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import PlainTextResponse, HTMLResponse, Response, JSONResponse
from pydantic import BaseModel
import pandas as pd
import io, os, json, datetime
from typing import Any, Dict, List

# ---- App ----
app = FastAPI(title="AURA Analytics API", version="0.2.0")

# ---- State (MVP) ----
DATAFRAME: pd.DataFrame | None = None
LAST_INGEST_INFO: Dict[str, Any] = {}

AURA_DATA_DIR = os.getenv("AURA_DATA_DIR", "/var/aura")
os.makedirs(AURA_DATA_DIR, exist_ok=True)

# ---- Models ----
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
    confidence: float
    metrics: List[str]
    complexity: str
    risks: List[str]
    priority: str
    summary: str
    teams: List[str]
    consequence_if_ignored: str
    comments: str = ""

# ---- Utils ----
def _read_any_to_df(upload: UploadFile) -> pd.DataFrame:
    name = (upload.filename or "").lower()
    raw = upload.file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty file")
    try:
        if name.endswith(".csv"):
            return pd.read_csv(io.BytesIO(raw))
        if name.endswith(".json"):
            return pd.read_json(io.BytesIO(raw))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse {name}: {e}")
    try:
        return pd.read_csv(io.BytesIO(raw))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unsupported format for {name}: {e}")

def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})
    for cand in ["started_at", "start_time", "timestamp", "ts", "date"]:
        if cand in df.columns:
            df[cand] = pd.to_datetime(df[cand], errors="coerce")
            break
    for cand in ["ai_used", "cws", "provisioned"]:
        if cand in df.columns:
            df[cand] = df[cand].astype(str).str.lower().isin(["1","true","yes","y","t"])
    if "duration_min" in df.columns:
        df["duration_min"] = pd.to_numeric(df["duration_min"], errors="coerce")
    return df

# простенькая QA-проверка «контракта данных»
EXPECTED_ANY_OF = [
    ("timestamp", ["started_at","start_time","timestamp","ts","date"]),
]
EXPECTED_FIELDS = ["user_id"]  # базово хотим user_id
OPTIONAL_FIELDS = ["ai_used","cws","provisioned","duration_min"]

def _contract_check(df: pd.DataFrame) -> dict:
    cols = set(df.columns)
    missing = [f for f in EXPECTED_FIELDS if f not in cols]
    any_of_missing = []
    for label, choices in EXPECTED_ANY_OF:
        if not any(c in cols for c in choices):
            any_of_missing.append({label: choices})
    status = (len(missing)==0 and len(any_of_missing)==0)
    return {"ok": status, "missing": missing, "any_of_missing": any_of_missing}

def _compute_metrics(df: pd.DataFrame) -> List[Metric]:
    metrics: List[Metric] = []
    cols = set(df.columns)
    if "user_id" in cols:
        metrics.append(Metric(key="AS", value=int(df["user_id"].nunique()),
                              description="Active seats (unique users)", computed=True))
    else:
        metrics.append(Metric(key="AS", value=None, description="Active seats (unique users)", computed=False))
    if "user_id" in cols:
        sessions_per_user = df.groupby("user_id").size()
        metrics.append(Metric(key="ARp", value=round(float((sessions_per_user>=3).mean()),3),
                              description="Adoption rate (proxy: users with ≥3 sessions)", computed=True))
    else:
        metrics.append(Metric(key="ARp", value=None, description="Adoption rate (proxy)", computed=False))
    if "ai_used" in cols and len(df):
        metrics.append(Metric(key="AIcov", value=round(float(df["ai_used"].mean()),3),
                              description="Share of sessions with AI usage", computed=True))
    else:
        metrics.append(Metric(key="AIcov", value=None, description="Share of sessions with AI usage", computed=False))
    if "cws" in cols:
        metrics.append(Metric(key="CWS", value=int(df["cws"].sum()),
                              description="Count of collaboration (Code With Me) sessions", computed=True))
    else:
        metrics.append(Metric(key="CWS", value=None, description="Count of collaboration sessions", computed=False))
    if "provisioned" in cols and len(df):
        metrics.append(Metric(key="ProvOK", value=round(float(df["provisioned"].mean()),3),
                              description="Provisioning success rate", computed=True))
    else:
        metrics.append(Metric(key="ProvOK", value=None, description="Provisioning success rate", computed=False))
    return metrics

def _derive_insights(df: pd.DataFrame, metrics: List[Metric]) -> List[Insight]:
    m = {x.key: x for x in metrics}
    insights: List[Insight] = []
    if m["AIcov"].computed and m["AIcov"].value is not None and m["AIcov"].value < 0.2:
        conf = max(0.4, min(0.9, len(df)/1000.0))
        insights.append(Insight(
            id="ai-low-coverage",
            title="Low AI feature coverage",
            hypothesis="AI features are underused across teams",
            problem="Potential productivity uplift from AI assistance is not realized",
            impact="Reduced throughput; longer time-to-ship",
            stakeholders=["DPE Manager","Team Leads","Developers"],
            domain="developer_productivity",
            data_fields=[c for c in df.columns if c in ["ai_used","user_id","started_at","timestamp"]],
            confidence=round(conf,2),
            metrics=["AIcov","ARp"],
            complexity="Medium",
            risks=["Over-attribution","Privacy concerns"],
            priority="High",
            summary="AI usage < 20%; consider enablement & better prompts.",
            teams=["Platform/DevEx","Security/Compliance"],
            consequence_if_ignored="AI ROI remains unrealized",
            comments=""
        ))
    if m["ProvOK"].computed and m["ProvOK"].value is not None and m["ProvOK"].value < 0.95:
        insights.append(Insight(
            id="provisioning-issues",
            title="Provisioning success below target",
            hypothesis="Provisioning errors block usage and adoption",
            problem="Users cannot start sessions reliably",
            impact="Lower adoption & satisfaction",
            stakeholders=["Platform Ops","IT"],
            domain="platform_reliability",
            data_fields=[c for c in df.columns if c in ["provisioned","user_id","started_at","timestamp"]],
            confidence=0.7,
            metrics=["ProvOK","ARp"],
            complexity="Low",
            risks=["Transient errors misread"],
            priority="High",
            summary="Prov success <95%; investigate errors and add retries.",
            teams=["Platform Ops","SRE"],
            consequence_if_ignored="Adoption stalls; reputation risk",
            comments=""
        ))
    if m["CWS"].computed and m["CWS"].value == 0:
        insights.append(Insight(
            id="collab-missing",
            title="Collaboration sessions not observed",
            hypothesis="Teams are not using collaboration features",
            problem="Missed opportunities for pair reviews/mentoring",
            impact="Slower onboarding; silos",
            stakeholders=["Team Leads","Developers"],
            domain="continuous_learning",
            data_fields=[c for c in df.columns if c in ["cws","user_id"]],
            confidence=0.6,
            metrics=["CWS","ARp"],
            complexity="Low",
            risks=["CWS not instrumented"],
            priority="Medium",
            summary="No collaboration sessions recorded; add enablement/docs.",
            teams=["DevEx","Developer Education"],
            consequence_if_ignored="Slower ramp-up; lower quality",
            comments=""
        ))
    return insights

def _metrics_md(metrics: List[Metric]) -> str:
    lines = ["## Metrics"]
    for x in metrics:
        status = "✅" if x.computed else "⚪"
        lines.append(f"- {status} **{x.key}**: {x.value} — _{x.description}_")
    return "\n".join(lines)

def _insights_md(ins: List[Insight]) -> str:
    if not ins:
        return "## Insights\n_No insights produced for current dataset._"
    out = ["## Insights"]
    for i in ins:
        out += [
            f"### {i.title} ({i.id})",
            f"- Hypothesis: {i.hypothesis}",
            f"- Problem: {i.problem}",
            f"- Impact: {i.impact}",
            f"- Stakeholders: {', '.join(i.stakeholders)}",
            f"- Domain: {i.domain}",
            f"- Metrics: {', '.join(i.metrics)}",
            f"- Confidence: {i.confidence}",
            f"- Priority: {i.priority} | Complexity: {i.complexity}",
            f"- Summary: {i.summary}",
            f"- Consequence if ignored: {i.consequence_if_ignored}",
            "",
        ]
    return "\n".join(out)

def _build_report(md_body: str) -> dict:
    return {
        "md": md_body,
        "html": f"""<!doctype html>
<html><head><meta charset="utf-8"><title>AURA Report</title>
<style>body{{font-family: -apple-system, Segoe UI, Roboto, Arial; max-width:900px; margin:40px auto; line-height:1.5}}
h1,h2,h3{{margin-top:1.2em}}</style></head>
<body>{__import__("markdown").markdown(md_body)}</body></html>"""
    }

def _log(kind: str, payload: dict):
    try:
        rec = {"ts": datetime.datetime.utcnow().isoformat()+"Z", "kind": kind, **payload}
        with open(os.path.join(AURA_DATA_DIR, "usage.log"), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False)+"\n")
    except Exception:
        pass

# ---- Endpoints ----
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    global DATAFRAME, LAST_INGEST_INFO
    df = _read_any_to_df(file)
    df = _normalize_df(df)
    DATAFRAME = df
    LAST_INGEST_INFO = {"rows": len(df), "cols": list(df.columns), "source": file.filename}
    _log("ingest", {"rows": len(df), "source": file.filename or ""})
    return {"status": "ok", "ingested": LAST_INGEST_INFO}

@app.post("/ingest/sample")
async def ingest_sample():
    global DATAFRAME, LAST_INGEST_INFO
    path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "sample_data", "ide_sessions.csv"))
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="sample_data/ide_sessions.csv not found")
    df = pd.read_csv(path)
    df = _normalize_df(df)
    DATAFRAME = df
    LAST_INGEST_INFO = {"rows": len(df), "cols": list(df.columns), "source": "sample_data/ide_sessions.csv"}
    _log("ingest_sample", {"rows": len(df)})
    return {"status": "ok", "ingested": LAST_INGEST_INFO}

@app.post("/analyze")
async def analyze():
    if DATAFRAME is None or len(DATAFRAME) == 0:
        raise HTTPException(status_code=400, detail="No data ingested yet")
    contract = _contract_check(DATAFRAME)
    metrics = _compute_metrics(DATAFRAME)
    _log("analyze", {"rows": len(DATAFRAME)})
    return {"status": "ok", "contract": contract, "metrics": [m.model_dump() for m in metrics], "ingest": LAST_INGEST_INFO}

@app.get("/insights")
async def insights():
    if DATAFRAME is None or len(DATAFRAME) == 0:
        raise HTTPException(status_code=400, detail="No data ingested yet")
    metrics = _compute_metrics(DATAFRAME)
    ins = _derive_insights(DATAFRAME, metrics)
    return {"status": "ok", "count": len(ins), "insights": [i.model_dump() for i in ins]}

@app.get("/report")
async def report(format: str = Query("md", pattern="^(md|html|pdf)$")):
    if DATAFRAME is None or len(DATAFRAME) == 0:
        raise HTTPException(status_code=400, detail="No data ingested yet")
    metrics = _compute_metrics(DATAFRAME)
    ins = _derive_insights(DATAFRAME, metrics)
    md = "\n".join(["# AURA Analytics — Report (MVP)","", _metrics_md(metrics), "", _insights_md(ins)])
    pkg = _build_report(md)
    _log("report", {"format": format})

    if format == "md":
        return PlainTextResponse(pkg["md"], media_type="text/markdown; charset=utf-8")
    if format == "html":
        return HTMLResponse(pkg["html"])
    # pdf
    try:
        from weasyprint import HTML  # lazy import
        pdf_bytes = HTML(string=pkg["html"]).write_pdf()
        return Response(content=pdf_bytes, media_type="application/pdf",
                        headers={"Content-Disposition":"inline; filename=aura-report.pdf"})
    except Exception as e:
        return JSONResponse(status_code=501, content={"status":"not_implemented","detail":str(e)})

@app.get("/admin/usage")
def usage():
    path = os.path.join(AURA_DATA_DIR, "usage.log")
    if not os.path.exists(path):
        return {"events": 0, "by_kind": {}}
    by_kind: Dict[str,int] = {}
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            total += 1
            try:
                kind = json.loads(line).get("kind","unknown")
                by_kind[kind] = by_kind.get(kind,0)+1
            except Exception:
                by_kind["broken"] = by_kind.get("broken",0)+1
    return {"events": total, "by_kind": by_kind}
