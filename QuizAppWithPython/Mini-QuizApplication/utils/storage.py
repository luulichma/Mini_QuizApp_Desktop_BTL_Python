import json, os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
DATA_FILE = os.path.abspath(DATA_FILE)

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
