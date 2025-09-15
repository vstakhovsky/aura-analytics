import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pipeline_end_to_end():
    # загрузка сэмпла
    r = client.post("/ingest/sample")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["ingested"]["rows"] > 0

    # анализ (метрики)
    r = client.post("/analyze")
    assert r.status_code == 200
    payload = r.json()
    assert payload["status"] == "ok"
    assert any(m["key"] == "AS" for m in payload["metrics"])

    # инсайты
    r = client.get("/insights")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

    # отчёт
    r = client.get("/report")
    assert r.status_code == 200
    assert r.text.startswith("# AURA Analytics")
