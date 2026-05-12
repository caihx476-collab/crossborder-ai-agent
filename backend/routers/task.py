from fastapi import APIRouter, Query
from backend.models.schemas import TaskSummary, DashboardStats
from backend.db.crud import get_tasks, get_dashboard_stats, search_tasks

router = APIRouter(prefix="/api", tags=["task"])


@router.get("/tasks", response_model=list[TaskSummary])
def list_tasks(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    return get_tasks(limit=limit, offset=offset)


@router.get("/tasks/search", response_model=list[TaskSummary])
def search_tasks_api(keyword: str = Query(..., min_length=1), limit: int = Query(20, ge=1, le=100)):
    return search_tasks(keyword=keyword, limit=limit)


@router.get("/stats", response_model=DashboardStats)
def stats():
    return get_dashboard_stats()
