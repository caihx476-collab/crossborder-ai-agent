import pymysql
from contextlib import contextmanager
from backend.config import settings
from backend.utils.logger import logger


def get_connection():
    return pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        charset="utf8mb4",
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.commit()
    finally:
        conn.close()

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                batch_id VARCHAR(64) PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                product_feature TEXT,
                region VARCHAR(64),
                platform VARCHAR(32) DEFAULT 'amazon',
                created_at VARCHAR(32),
                excel_path VARCHAR(512)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id VARCHAR(128) PRIMARY KEY,
                batch_id VARCHAR(64) NOT NULL,
                item_type VARCHAR(32) NOT NULL,
                content TEXT NOT NULL,
                status VARCHAR(16) DEFAULT 'Pending',
                created_at VARCHAR(32),
                INDEX idx_items_batch_id (batch_id),
                INDEX idx_items_status (status),
                INDEX idx_items_type (item_type),
                FOREIGN KEY (batch_id) REFERENCES tasks(batch_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            try:
                cursor.execute("CREATE INDEX idx_tasks_created_at ON tasks (created_at)")
            except Exception:
                pass
        conn.commit()
    logger.info("MySQL数据库初始化完成")
