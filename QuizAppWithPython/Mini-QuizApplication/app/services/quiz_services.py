from app.databases.collections import QUIZZES, QUESTIONS, OPTIONS
from app.databases.schema import quiz_schema, question_schema, option_schema
from typing import List, Dict, Any, Optional
from bson import ObjectId


def create_quiz(user_id: str, title: str, description: str) -> str:
	"""Create a quiz document and return its inserted id as string."""
	doc = quiz_schema(user_id, title, description)
	res = QUIZZES.insert_one(doc)
	return str(res.inserted_id)


def add_question(quiz_id: str, question_title: str, correct_answer: str, options: Optional[List[Dict[str, Any]]] = None) -> str:
	"""Add a question to QUESTIONS collection; options is a list of {'text':..., 'display_order':...}.
	Returns question id string."""
	q = question_schema(quiz_id, question_title, correct_answer)
	res = QUESTIONS.insert_one(q)
	qid = str(res.inserted_id)

	if options:
		for opt in options:
			opt_doc = option_schema(qid, opt.get("text"), opt.get("display_order", 0))
			OPTIONS.insert_one(opt_doc)

	return qid


def list_quizzes() -> List[Dict[str, Any]]:
	out = []
	for q in QUIZZES.find():
		out.append({
			"_id": str(q.get("_id")),
			"title": q.get("title"),
			"description": q.get("description"),
			"created_at": q.get("created_at")
		})
	return out
