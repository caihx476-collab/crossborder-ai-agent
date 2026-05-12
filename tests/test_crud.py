import pytest
from backend.db.database import init_db, get_db
from backend.db.crud import (
    save_task_and_items,
    get_tasks,
    get_items_by_batch,
    update_item_status,
    batch_update_status,
    get_dashboard_stats,
)
from backend.models.schemas import ContentItem, GenerateResponse


@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield


def _make_response(batch_id="20260101_120000"):
    return GenerateResponse(
        batch_id=batch_id,
        items=[
            ContentItem(item_id=f"{batch_id}_title_1", batch_id=batch_id, item_type="Title", content="Test Title", status="Pending"),
            ContentItem(item_id=f"{batch_id}_keyword_1", batch_id=batch_id, item_type="SEO Keyword", content="test keyword", status="Pending"),
        ],
        provider="TestProvider",
        created_at="2026-01-01 12:00:00",
    )


def test_save_and_get_tasks():
    resp = _make_response()
    save_task_and_items(resp, "TestProduct", "Feature", "US", "amazon")
    tasks = get_tasks()
    assert len(tasks) >= 1
    assert tasks[0].product_name == "TestProduct"


def test_get_items_by_batch():
    resp = _make_response("20260102_120000")
    save_task_and_items(resp, "Product2", "Feature2", "EU", "ebay")
    items = get_items_by_batch("20260102_120000")
    assert len(items) == 2


def test_update_item_status():
    resp = _make_response("20260103_120000")
    save_task_and_items(resp, "Product3", "Feature3", "US", "amazon")
    update_item_status("20260103_120000_title_1", "Approved")
    items = get_items_by_batch("20260103_120000")
    approved = [i for i in items if i.status == "Approved"]
    assert len(approved) == 1


def test_batch_update_status():
    resp = _make_response("20260104_120000")
    save_task_and_items(resp, "Product4", "Feature4", "US", "amazon")
    batch_update_status([
        {"item_id": "20260104_120000_title_1", "status": "Approved"},
        {"item_id": "20260104_120000_keyword_1", "status": "Rejected"},
    ])
    items = get_items_by_batch("20260104_120000")
    statuses = {i.item_id: i.status for i in items}
    assert statuses["20260104_120000_title_1"] == "Approved"
    assert statuses["20260104_120000_keyword_1"] == "Rejected"


def test_dashboard_stats():
    resp = _make_response("20260105_120000")
    save_task_and_items(resp, "Product5", "Feature5", "US", "amazon")
    stats = get_dashboard_stats()
    assert stats.total_tasks >= 1
    assert stats.total_items >= 2
