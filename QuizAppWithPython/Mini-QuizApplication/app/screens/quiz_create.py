from kivy.uix.screenmanager import Screen
from utils.storage import load_quizzes, save_quizzes
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class QuizCreateScreen(Screen):
    quiz_name = ObjectProperty(None)
    quiz_desc = ObjectProperty(None)
    question_input = ObjectProperty(None)
    answer_input = ObjectProperty(None)

    def add_quiz(self):
        name = self.quiz_name.text.strip()
        desc = self.quiz_desc.text.strip()
        question = self.question_input.text.strip()
        answer = self.answer_input.text.strip()

        if not name or not question or not answer:
            Popup(title="Lỗi", content=Label(text="Vui lòng nhập đầy đủ thông tin!")).open()
            return

        quizzes = load_quizzes()
        quizzes.append({
            "name": name,
            "description": desc,
            "questions": [{
                "question": question,
                "answer": answer
            }]
        })
        save_quizzes(quizzes)
        Popup(title="Thành công", content=Label(text="Quiz đã được tạo!")).open()
        self.quiz_name.text = ""
        self.quiz_desc.text = ""
        self.question_input.text = ""
        self.answer_input.text = ""
