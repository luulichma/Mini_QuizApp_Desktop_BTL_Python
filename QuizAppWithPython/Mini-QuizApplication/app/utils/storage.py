import json, os

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "users.json")
DATA_FILE = os.path.abspath(DATA_FILE)
QUIZ_FILE = os.path.join(BASE_DIR, "..", "data", "quizzes.json")
QUIZ_FILE = os.path.abspath(QUIZ_FILE)
RESULT_FILE = os.path.join(BASE_DIR, "..", "data", "results.json")
RESULT_FILE = os.path.abspath(RESULT_FILE)

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def load_quizzes():
    if not os.path.exists(QUIZ_FILE):
        return []
    with open(QUIZ_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_quizzes(quizzes):
    with open(QUIZ_FILE, "w", encoding="utf-8") as f:
        json.dump(quizzes, f, ensure_ascii=False, indent=4)

def load_results():
    if not os.path.exists(RESULT_FILE):
        return []
    with open(RESULT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_results(results):
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)