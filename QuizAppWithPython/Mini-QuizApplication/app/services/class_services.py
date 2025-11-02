from app.databases.collections import CLASSES, CLASS_STUDENTS, USERS
from app.databases.schema import class_schema, class_student_schema
from typing import List, Dict, Any, Optional
from bson import ObjectId

def create_class(teacher_id: str, class_name: str, description: str) -> str:
    doc = class_schema(teacher_id, class_name, description)
    res = CLASSES.insert_one(doc)
    return str(res.inserted_id)

def list_classes_by_teacher(teacher_id: str) -> List[Dict[str, Any]]:
    try:
        tid = ObjectId(teacher_id)
    except Exception:
        return []

    cursor = CLASSES.find({"teacher_id": tid}).sort("created_at", -1)
    return [
        {
            "_id": str(c["_id"]),
            "class_name": c["class_name"],
            "description": c.get("description", ""),
            "created_at": c.get("created_at")
        }
        for c in cursor
    ]

def get_class_details(class_id: str) -> Optional[Dict[str, Any]]:
    try:
        cid = ObjectId(class_id)
    except Exception:
        return None

    class_data = CLASSES.find_one({"_id": cid})
    if not class_data:
        return None
    
    class_data["_id"] = str(class_data["_id"])
    return class_data

def add_student_to_class(class_id: str, student_id: str) -> bool:
    student = USERS.find_one({"_id": ObjectId(student_id), "role": "player"})
    if not student:
        return False
    
    # Check if student is already in class
    existing_entry = CLASS_STUDENTS.find_one({"class_id": ObjectId(class_id), "student_id": student["_id"]})
    if existing_entry:
        return False # Student already in class

    doc = class_student_schema(class_id, str(student["_id"]))
    CLASS_STUDENTS.insert_one(doc)
    return True

def list_students_in_class(class_id: str) -> List[Dict[str, Any]]:
    try:
        cid = ObjectId(class_id)
    except Exception:
        return []

    pipeline = [
        {'$match': {'class_id': cid}},
        {'$lookup': {
            'from': 'users',
            'localField': 'student_id',
            'foreignField': '_id',
            'as': 'student_info'
        }},
        {'$unwind': '$student_info'},
        {'$project': {
            '_id': '$student_info._id',
            'name': '$student_info.name',
            'username': '$student_info.username',
            'enrolled_at': 1
        }}
    ]
    
    cursor = CLASS_STUDENTS.aggregate(pipeline)
    return [
        {
            "_id": str(s["_id"]),
            "name": s["name"],
            "username": s["username"],
            "enrolled_at": s["enrolled_at"]
        }
        for s in cursor
    ]

def remove_student_from_class(class_id: str, student_id: str) -> bool:
    result = CLASS_STUDENTS.delete_one({"class_id": ObjectId(class_id), "student_id": ObjectId(student_id)})
    return result.deleted_count > 0

def delete_class(class_id: str) -> bool:
    try:
        cid = ObjectId(class_id)
    except Exception:
        return False
    
    # Delete all student enrollments for this class
    CLASS_STUDENTS.delete_many({"class_id": cid})
    
    # Delete the class itself
    result = CLASSES.delete_one({"_id": cid})
    return result.deleted_count > 0
