import json
import os
from datetime import datetime


HISTORY_PATH = "data/history.json"


def load_history():

    if not os.path.exists(HISTORY_PATH):
        return []

    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(data):

    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_history(
    batch_id,
    product_info,
    items,
    excel_path
):

    history = load_history()

    record = {

        "batch_id": batch_id,

        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "product_info": product_info,

        "items": items,

        "excel_path": excel_path
    }

    history.append(record)

    save_history(history)