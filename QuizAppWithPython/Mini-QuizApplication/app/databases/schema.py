from datetime import datetime
from bson import ObjectId

# ===== USERS =====
def user_schema(name, email, username, password, role="player", average_score=0.0):
    return {
        "name": name,
        "email": email,
        "username": username,
        "password": password,
        "role": role,  # "creator" hoặc "player"
        "average_score": average_score
    }

# ===== QUIZZES =====
def quiz_schema(user_id, title, description, duration=0):
    return {
        "user_id": ObjectId(user_id),
        "title": title,
        "description": description,
        "duration": duration,
        "created_at": datetime.utcnow()
    }

# ===== QUESTIONS =====
def question_schema(quiz_id, question_title, correct_answer):
    return {
        "quiz_id": ObjectId(quiz_id),
        "question_title": question_title,
        "correct_answer": correct_answer
    }

# ===== OPTIONS =====
def option_schema(question_id, text, display_order):
    return {
        "question_id": ObjectId(question_id),
        "text": text,
        "display_order": display_order
    }

# ===== RESULTS =====
def result_schema(user_id, quiz_id, score):
    return {
        "user_id": ObjectId(user_id),
        "quiz_id": ObjectId(quiz_id),
        "score": score,
        "submitted_at": datetime.utcnow()
    }

# ===== CLASSES =====
def class_schema(teacher_id, class_name, description):
    return {
        "teacher_id": ObjectId(teacher_id),
        "class_name": class_name,
        "description": description,
        "created_at": datetime.utcnow()
    }

# ===== CLASS_STUDENTS =====
def class_student_schema(class_id, student_id):
    return {
        "class_id": ObjectId(class_id),
        "student_id": ObjectId(student_id),
        "enrolled_at": datetime.utcnow()
    }
