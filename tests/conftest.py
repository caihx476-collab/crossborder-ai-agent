import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["AI_PROVIDER"] = "minimax"
os.environ["MINIMAX_API_KEY"] = "test-key"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "3306"
os.environ["DB_USER"] = "root"
os.environ["DB_PASSWORD"] = ""
os.environ["DB_NAME"] = "crossborder_ai_test"


@pytest.fixture(autouse=True)
def cleanup_test_db():
    yield
    import pymysql
    try:
        conn = pymysql.connect(
            host="localhost", port=3306, user="root", password="",
            charset="utf8mb4",
        )
        with conn.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS crossborder_ai_test")
        conn.commit()
        conn.close()
    except Exception:
        pass
