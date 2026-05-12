import httpx
import streamlit as st
from typing import Optional

API_BASE = "http://localhost:8000/api"


def _get_client() -> httpx.Client:
    return httpx.Client(base_url=API_BASE, timeout=120.0)


def api_generate(product: dict, content_types: list[str], provider: Optional[str] = None) -> Optional[dict]:
    try:
        with _get_client() as client:
            payload = {"product": product, "content_types": content_types}
            if provider:
                payload["provider"] = provider
            resp = client.post("/generate", json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.ConnectError:
        st.error("无法连接后端服务，请确认 FastAPI 已启动")
        return None
    except httpx.HTTPStatusError as e:
        detail = e.response.json().get("detail", str(e))
        st.error(f"生成失败: {detail}")
        return None
    except Exception as e:
        st.error(f"请求异常: {e}")
        return None


def api_get_tasks(limit: int = 20, offset: int = 0) -> list[dict]:
    try:
        with _get_client() as client:
            resp = client.get("/tasks", params={"limit": limit, "offset": offset})
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return []


def api_get_items(batch_id: str) -> Optional[list[dict]]:
    try:
        with _get_client() as client:
            resp = client.get(f"/tasks/{batch_id}/items")
            resp.raise_for_status()
            return resp.json().get("items", [])
    except Exception:
        return None


def api_update_status(item_id: str, action: str) -> bool:
    try:
        with _get_client() as client:
            resp = client.put(f"/items/{item_id}/status", params={"action": action})
            resp.raise_for_status()
            return True
    except Exception:
        return False


def api_batch_review(items: list[dict]) -> bool:
    try:
        with _get_client() as client:
            resp = client.post("/items/batch-review", json={"items": items})
            resp.raise_for_status()
            return True
    except Exception:
        return False


def api_get_stats() -> dict:
    try:
        with _get_client() as client:
            resp = client.get("/stats")
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return {"total_tasks": 0, "total_items": 0, "pending_count": 0, "approved_count": 0, "rejected_count": 0}


def api_search_tasks(keyword: str) -> list[dict]:
    try:
        with _get_client() as client:
            resp = client.get("/tasks/search", params={"keyword": keyword})
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return []


def api_export_excel(batch_id: str) -> Optional[bytes]:
    try:
        with _get_client() as client:
            resp = client.get(f"/export/{batch_id}")
            resp.raise_for_status()
            return resp.content
    except Exception:
        return None
