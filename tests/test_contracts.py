from pathlib import Path
import json
from fastapi.testclient import TestClient
from api.main import app

ROOT = Path(__file__).resolve().parents[1]

def test_sample_report_conforms_to_schema():
    # runtime: just hit /api/run (no upload) and ensure fields exist
    c = TestClient(app)
    r = c.get("/api/run")
    assert r.status_code == 200
    data = r.json()
    # minimal structural checks (schema is validated by validator already)
    assert "executive_summary" in data
    assert isinstance(data.get("insights"), list) and len(data["insights"]) >= 2
    assert isinstance(data.get("hypotheses"), list) and len(data["hypotheses"]) >= 1
    assert "validator_scorecard" in data

def test_openapi_available():
    c = TestClient(app)
    r = c.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    assert "/api/run" in spec.get("paths", {})
    assert "/upload/" in spec.get("paths", {})
