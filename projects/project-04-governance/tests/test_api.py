from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_fairness_endpoint():
    r = client.post("/v1/fairness", json={
        "y_true": [1, 0, 1, 0, 1, 0, 1, 0],
        "y_pred": [1, 0, 1, 0, 1, 0, 1, 0],
        "sensitive": ["a", "b", "a", "b", "a", "b", "a", "b"],
    })
    assert r.status_code == 200
    body = r.json()
    assert body["disparate_impact"] == 1.0
    assert body["passes_four_fifths_rule"]


def test_audit_logs_after_fairness_call():
    client.post("/v1/fairness", json={
        "y_true": [1, 0], "y_pred": [1, 0], "sensitive": ["a", "b"],
    })
    events = client.get("/v1/audit").json()["events"]
    assert any(e["event_type"] == "fairness.assess" for e in events)
    assert client.get("/v1/audit/verify").json()["valid"]
