import json


def load_review_status():
    with open("data/review_status.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_review_status(data):
    with open("data/review_status.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)