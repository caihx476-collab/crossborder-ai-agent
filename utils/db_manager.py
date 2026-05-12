import sqlite3
import os


DB_PATH = "data/app.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        batch_id TEXT PRIMARY KEY,
        product_name TEXT,
        product_feature TEXT,
        region TEXT,
        created_at TEXT,
        excel_path TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id TEXT PRIMARY KEY,
        batch_id TEXT,
        item_type TEXT,
        content TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
def save_task(batch_id, product_info, excel_path, created_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks (
        batch_id,
        product_name,
        product_feature,
        region,
        created_at,
        excel_path
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        batch_id,
        product_info["name"],
        product_info["feature"],
        product_info["region"],
        created_at,
        excel_path
    ))

    conn.commit()
    conn.close()


def save_items(items, batch_id):
    conn = get_connection()
    cursor = conn.cursor()

    for item in items:
        cursor.execute("""
        INSERT INTO items (
            item_id,
            batch_id,
            item_type,
            content,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            item["item_id"],
            batch_id,
            item["type"],
            item["content"],
            item["status"]
        ))

    conn.commit()
    conn.close()
def get_recent_tasks(limit=10):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        batch_id,
        product_name,
        product_feature,
        region,
        created_at,
        excel_path
    FROM tasks
    ORDER BY created_at DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    result = []

    for row in rows:

        result.append({
            "batch_id": row[0],
            "product_name": row[1],
            "product_feature": row[2],
            "region": row[3],
            "created_at": row[4],
            "excel_path": row[5]
        })

    return result
def get_items_by_batch(batch_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        item_id,
        item_type,
        content,
        status
    FROM items
    WHERE batch_id = ?
    """, (batch_id,))

    rows = cursor.fetchall()

    conn.close()

    result = []

    for row in rows:

        result.append({
            "item_id": row[0],
            "type": row[1],
            "content": row[2],
            "status": row[3]
        })

    return result
#查询
def search_tasks(keyword, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        batch_id,
        product_name,
        product_feature,
        region,
        created_at,
        excel_path
    FROM tasks
    WHERE product_name LIKE ?
    ORDER BY created_at DESC
    LIMIT ?
    """, (f"%{keyword}%", limit))

    rows = cursor.fetchall()
    conn.close()

    result = []

    for row in rows:
        result.append({
            "batch_id": row[0],
            "product_name": row[1],
            "product_feature": row[2],
            "region": row[3],
            "created_at": row[4],
            "excel_path": row[5]
        })

    return result
#更新状态
def update_item_status(item_id, new_status):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE items
    SET status = ?
    WHERE item_id = ?
    """, (new_status, item_id))

    conn.commit()

    conn.close()
#获得总数
def get_dashboard_stats():

    conn = get_connection()

    cursor = conn.cursor()

    # 总任务数
    cursor.execute("""
    SELECT COUNT(*)
    FROM tasks
    """)

    total_tasks = cursor.fetchone()[0]

    # 总内容数
    cursor.execute("""
    SELECT COUNT(*)
    FROM items
    """)

    total_items = cursor.fetchone()[0]

    # Approved数量
    cursor.execute("""
    SELECT COUNT(*)
    FROM items
    WHERE status = 'Approved'
    """)

    approved_count = cursor.fetchone()[0]

    # Rejected数量
    cursor.execute("""
    SELECT COUNT(*)
    FROM items
    WHERE status = 'Rejected'
    """)

    rejected_count = cursor.fetchone()[0]

    # Pending数量
    cursor.execute("""
    SELECT COUNT(*)
    FROM items
    WHERE status = 'Pending'
    """)

    pending_count = cursor.fetchone()[0]

    conn.close()

    return {
        "total_tasks": total_tasks,
        "total_items": total_items,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "pending_count": pending_count
    }
#GROUP BY 分组统计
def get_status_group_stats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT status, COUNT(*)
    FROM items
    GROUP BY status
    """)

    rows = cursor.fetchall()

    conn.close()

    result = {}

    for row in rows:
        status = row[0]
        count = row[1]

        result[status] = count

    return result
def get_item_type_stats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT item_type, COUNT(*)
    FROM items
    GROUP BY item_type
    """)

    rows = cursor.fetchall()

    conn.close()

    result = {}

    for row in rows:
        item_type = row[0]
        count = row[1]

        result[item_type] = count

    return result