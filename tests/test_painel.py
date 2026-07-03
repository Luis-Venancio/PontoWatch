from fastapi.testclient import TestClient

from app.main import app
from app.api import painel


def test_resumo_returns_empty_payload_when_db_is_unavailable(monkeypatch):
    def raise_runtime_error():
        raise RuntimeError("Supabase credentials not configured")

    monkeypatch.setattr(painel, "get_supabase", raise_runtime_error)

    with TestClient(app) as client:
        response = client.get("/painel/resumo?dia=2026-06-24")

    assert response.status_code == 200
    body = response.json()
    assert body["data"] == "2026-06-24"
    assert body["total"] == 0
    assert body["conformes"] == 0
