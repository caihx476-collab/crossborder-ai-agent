import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.database import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup():
    init_db()
    yield


def test_health_check():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_get_stats():
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_tasks" in data
    assert "total_items" in data


def test_get_tasks_empty():
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_items_not_found():
    resp = client.get("/api/tasks/nonexistent/items")
    assert resp.status_code == 404
