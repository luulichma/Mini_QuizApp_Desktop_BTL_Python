from app.databases.collections import QUIZZES, QUESTIONS, OPTIONS, RESULTS
from app.databases.schema import quiz_schema, question_schema, option_schema, result_schema
from typing import List, Dict, Any, Optional
from bson import ObjectId

def create_quiz(user_id: str, title: str, description: str) -> str:
	doc = quiz_schema(user_id, title, description)
	res = QUIZZES.insert_one(doc)
	return str(res.inserted_id)

def add_question(quiz_id: str, question_title: str, correct_answer: str, options: Optional[List[Dict[str, Any]]] = None) -> str:
	q = question_schema(quiz_id, question_title, correct_answer)
	res = QUESTIONS.insert_one(q)
	qid = str(res.inserted_id)

	if options:
		for opt in options:
			opt_doc = option_schema(qid, opt.get("text"), opt.get("display_order", 0))
			OPTIONS.insert_one(opt_doc)

	return qid

def list_quizzes_by_user(user_id: str) -> List[Dict[str, Any]]:
    try:
        uid = ObjectId(user_id)
    except Exception:
        return []

    cursor = QUIZZES.find({"user_id": uid}).sort("created_at", -1)
    return [
        {
            "_id": str(q["_id"]),
            "title": q["title"],
            "description": q.get("description", ""),
            "created_at": q.get("created_at")
        }
        for q in cursor
    ]


def list_quizzes() -> List[Dict[str, Any]]:
	"""Return all quizzes (for students)."""
	out: List[Dict[str, Any]] = []
	for q in QUIZZES.find().sort("created_at", -1):
		out.append({
			"_id": str(q.get("_id")),
			"title": q.get("title"),
			"description": q.get("description", ""),
			"created_at": q.get("created_at")
		})
	return out

def delete_quiz(quiz_id: str) -> int:
    q_id = ObjectId(quiz_id)
    questions_cursor = QUESTIONS.find({"quiz_id": q_id}, {"_id": 1})
    question_ids = [q["_id"] for q in questions_cursor]
    if question_ids:
        OPTIONS.delete_many({"question_id": {"$in": question_ids}})
    QUESTIONS.delete_many({"quiz_id": q_id})
    result = QUIZZES.delete_one({"_id": q_id})
    return result.deleted_count

def get_quiz_details(quiz_id: str) -> Optional[Dict[str, Any]]:
    try:
        q_id = ObjectId(quiz_id)
    except Exception:
        return None

    quiz = QUIZZES.find_one({"_id": q_id})
    if not quiz:
        return None

    questions = []
    questions_cursor = QUESTIONS.find({"quiz_id": q_id})
    for q in questions_cursor:
        options = []
        options_cursor = OPTIONS.find({"question_id": q["_id"]}).sort("display_order", 1)
        for o in options_cursor:
            options.append({
                "_id": str(o["_id"]),
                "text": o["text"],
            })
        questions.append({
            "_id": str(q["_id"]),
            "question_title": q["question_title"],
            "correct_answer": q["correct_answer"],
            "options": options
        })
    
    quiz['questions'] = questions
    return quiz

def update_quiz(quiz_id: str, title: str, description: str, questions_data: List[Dict[str, Any]]) -> None:
    q_id = ObjectId(quiz_id)
    QUIZZES.update_one(
        {"_id": q_id},
        {"$set": {"title": title, "description": description}}
    )
    old_questions_cursor = QUESTIONS.find({"quiz_id": q_id}, {"_id": 1})
    old_question_ids = [q["_id"] for q in old_questions_cursor]
    if old_question_ids:
        OPTIONS.delete_many({"question_id": {"$in": old_question_ids}})
    QUESTIONS.delete_many({"quiz_id": q_id})
    for q_data in questions_data:
        add_question(
            quiz_id=quiz_id,
            question_title=q_data['question_title'],
            correct_answer=q_data['correct_answer'],
            options=q_data['options']
        )

def get_results_by_user(user_id: str) -> List[Dict[str, Any]]:
    try:
        uid = ObjectId(user_id)
    except Exception:
        return []

    results_cursor = RESULTS.find({"user_id": uid}).sort("submitted_at", -1)
    
    history = []
    for res in results_cursor:
        quiz_info = QUIZZES.find_one({"_id": res["quiz_id"]})
        history.append({
            "quiz_title": quiz_info.get("title", "Không rõ tên") if quiz_info else "Quiz đã bị xóa",
            "score": res.get("score", "N/A"),
            "submitted_at": res.get("submitted_at")
        })
        
    return history

def save_quiz_result(user_id: str, quiz_id: str, score: str):
    """Saves a student's quiz result to the database."""
    doc = result_schema(user_id=user_id, quiz_id=quiz_id, score=score)
    RESULTS.insert_one(doc)
