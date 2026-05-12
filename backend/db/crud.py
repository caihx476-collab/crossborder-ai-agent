from datetime import datetime
from typing import Optional
from backend.db.database import get_db, init_db
from backend.models.schemas import (
    ContentItem, TaskSummary, DashboardStats, GenerateResponse,
)
from backend.utils.logger import logger
from backend.utils.exceptions import NotFoundException, DatabaseException


def save_task_and_items(response: GenerateResponse, product_name: str, product_feature: str,
                        region: str, platform: str, excel_path: Optional[str] = None):
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tasks (batch_id, product_name, product_feature, region, platform, created_at, excel_path) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (response.batch_id, product_name, product_feature, region, platform, response.created_at, excel_path),
                )
                for item in response.items:
                    cursor.execute(
                        "INSERT INTO items (item_id, batch_id, item_type, content, status, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
                        (item.item_id, item.batch_id, item.item_type, item.content, item.status, item.created_at),
                    )
            conn.commit()
        logger.info(f"保存任务 {response.batch_id}，共 {len(response.items)} 项内容")
    except Exception as e:
        raise DatabaseException(f"保存任务失败: {e}")


def get_tasks(limit: int = 20, offset: int = 0) -> list[TaskSummary]:
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT t.batch_id, t.product_name, t.region, t.platform, t.created_at, t.excel_path, "
                    "COUNT(i.item_id) as total_items, "
                    "SUM(CASE WHEN i.status='Pending' THEN 1 ELSE 0 END) as pending_count, "
                    "SUM(CASE WHEN i.status='Approved' THEN 1 ELSE 0 END) as approved_count, "
                    "SUM(CASE WHEN i.status='Rejected' THEN 1 ELSE 0 END) as rejected_count "
                    "FROM tasks t LEFT JOIN items i ON t.batch_id = i.batch_id "
                    "GROUP BY t.batch_id ORDER BY t.created_at DESC LIMIT %s OFFSET %s",
                    (limit, offset),
                )
                rows = cursor.fetchall()
            return [
                TaskSummary(
                    batch_id=r["batch_id"],
                    product_name=r["product_name"],
                    region=r["region"],
                    platform=r["platform"],
                    total_items=r["total_items"] or 0,
                    pending_count=r["pending_count"] or 0,
                    approved_count=r["approved_count"] or 0,
                    rejected_count=r["rejected_count"] or 0,
                    created_at=r["created_at"],
                    excel_path=r["excel_path"],
                )
                for r in rows
            ]
    except Exception as e:
        raise DatabaseException(f"获取任务列表失败: {e}")


def get_items_by_batch(batch_id: str) -> list[ContentItem]:
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT item_id, batch_id, item_type, content, status, created_at FROM items WHERE batch_id = %s ORDER BY item_type, item_id",
                    (batch_id,),
                )
                rows = cursor.fetchall()
            if not rows:
                raise NotFoundException(f"任务 {batch_id} 不存在")
            return [
                ContentItem(
                    item_id=r["item_id"],
                    batch_id=r["batch_id"],
                    item_type=r["item_type"],
                    content=r["content"],
                    status=r["status"],
                    created_at=r["created_at"],
                )
                for r in rows
            ]
    except NotFoundException:
        raise
    except Exception as e:
        raise DatabaseException(f"获取任务内容失败: {e}")


def update_item_status(item_id: str, new_status: str):
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE items SET status = %s WHERE item_id = %s",
                    (new_status, item_id),
                )
                affected = cursor.rowcount
            conn.commit()
            if affected == 0:
                raise NotFoundException(f"内容项 {item_id} 不存在")
        logger.info(f"更新 {item_id} 状态为 {new_status}")
    except NotFoundException:
        raise
    except Exception as e:
        raise DatabaseException(f"更新状态失败: {e}")


def batch_update_status(items: list[dict]):
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                for item in items:
                    cursor.execute(
                        "UPDATE items SET status = %s WHERE item_id = %s",
                        (item["status"], item["item_id"]),
                    )
            conn.commit()
        logger.info(f"批量更新 {len(items)} 项状态")
    except Exception as e:
        raise DatabaseException(f"批量更新状态失败: {e}")


def get_dashboard_stats() -> DashboardStats:
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as cnt FROM tasks")
                total_tasks = cursor.fetchone()["cnt"]
                cursor.execute("SELECT COUNT(*) as cnt FROM items")
                total_items = cursor.fetchone()["cnt"]
                cursor.execute("SELECT COUNT(*) as cnt FROM items WHERE status='Pending'")
                pending = cursor.fetchone()["cnt"]
                cursor.execute("SELECT COUNT(*) as cnt FROM items WHERE status='Approved'")
                approved = cursor.fetchone()["cnt"]
                cursor.execute("SELECT COUNT(*) as cnt FROM items WHERE status='Rejected'")
                rejected = cursor.fetchone()["cnt"]
        return DashboardStats(
            total_tasks=total_tasks,
            total_items=total_items,
            pending_count=pending,
            approved_count=approved,
            rejected_count=rejected,
        )
    except Exception as e:
        raise DatabaseException(f"获取统计数据失败: {e}")


def search_tasks(keyword: str, limit: int = 20) -> list[TaskSummary]:
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT t.batch_id, t.product_name, t.region, t.platform, t.created_at, t.excel_path, "
                    "COUNT(i.item_id) as total_items, "
                    "SUM(CASE WHEN i.status='Pending' THEN 1 ELSE 0 END) as pending_count, "
                    "SUM(CASE WHEN i.status='Approved' THEN 1 ELSE 0 END) as approved_count, "
                    "SUM(CASE WHEN i.status='Rejected' THEN 1 ELSE 0 END) as rejected_count "
                    "FROM tasks t LEFT JOIN items i ON t.batch_id = i.batch_id "
                    "WHERE t.product_name LIKE %s "
                    "GROUP BY t.batch_id ORDER BY t.created_at DESC LIMIT %s",
                    (f"%{keyword}%", limit),
                )
                rows = cursor.fetchall()
            return [
                TaskSummary(
                    batch_id=r["batch_id"],
                    product_name=r["product_name"],
                    region=r["region"],
                    platform=r["platform"],
                    total_items=r["total_items"] or 0,
                    pending_count=r["pending_count"] or 0,
                    approved_count=r["approved_count"] or 0,
                    rejected_count=r["rejected_count"] or 0,
                    created_at=r["created_at"],
                    excel_path=r["excel_path"],
                )
                for r in rows
            ]
    except Exception as e:
        raise DatabaseException(f"搜索任务失败: {e}")
