# database/db_connection.py
from pymongo import MongoClient

def get_db():
    """
    Kết nối tới MongoDB (thay URI bằng của bạn)
    """
    uri = "mongodb://localhost:27017"  # hoặc dùng MongoDB Atlas URI
    client = MongoClient(uri)
    db = client["MiniQuizApp"]
    return db
