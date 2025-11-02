# database/collections.py
from .db_connection import get_db

db = get_db()

USERS = db["users"]
QUIZZES = db["quizzes"]
QUESTIONS = db["questions"]
OPTIONS = db["options"]
RESULTS = db["results"]
CLASSES = db["classes"]
CLASS_STUDENTS = db["class_students"]
