from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import List

app = FastAPI(title="AURA Analytics API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)):
    # TODO: parse CSV/JSON and persist to DB (stub for MVP)
    names = [f.filename for f in files]
    return {"ingested": names, "note": "stub — implement persistence"}

@app.post("/analyze")
def analyze():
    # TODO: compute metrics & insights (stub)
    return {"status": "queued", "note": "stub — implement compute pipeline"}

@app.get("/insights")
def insights():
    # TODO: return computed insights (stub)
    return {"insights": [
        {"title": "AI features underutilized in Team A", "impact": "medium", "confidence": 0.7},
        {"title": "Provisioning failures spike on vX.Y", "impact": "high", "confidence": 0.8},
        {"title": "Collaboration session length dropping", "impact": "low", "confidence": 0.6},
    ]}

@app.get("/report", response_class=PlainTextResponse)
def report():
    # TODO: generate Markdown report dynamically
    md = """# AURA Analytics — Report (MVP)

- Status: demo
- Insights (3):
  1) AI features underutilized in Team A (confidence 0.7)
  2) Provisioning failures spike on vX.Y (confidence 0.8)
  3) Collaboration session length dropping (confidence 0.6)
"""
    return md
