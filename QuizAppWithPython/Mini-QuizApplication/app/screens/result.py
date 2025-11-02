from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from app.services import quiz_services

class ResultScreen(Screen):
    quiz_id = StringProperty(None)
    student_answers = DictProperty({})
    quiz_data = DictProperty({})
    score = StringProperty("")

    def on_enter(self, *args):
        """Called when the screen is entered. Loads the quiz data and displays the results."""
        self.quiz_data = quiz_services.get_quiz_details(self.quiz_id)
        if not self.quiz_data:
            self.go_back()
            return
        self.display_results()

    def display_results(self):
        """Calculates and displays the quiz results."""
        correct_answers = 0
        total_questions = len(self.quiz_data.get('questions', []))

        if total_questions == 0:
            self.go_back()
            return

        results_container = self.ids.results_container
        results_container.clear_widgets()

        for i, question in enumerate(self.quiz_data['questions']):
            question_id = question['_id']
            student_answer = self.student_answers.get(question_id)
            correct_answer = question['correct_answer']
            
            result_text = f"Câu {i+1}: {question['question_title']}\n"
            result_text += f"Đáp án của bạn: {student_answer}"
            
            result_label = Label(text=result_text, size_hint_y=None, height=100)
            if student_answer == correct_answer:
                correct_answers += 1
                result_label.color = (0, 1, 0, 1)  # Green for correct
            else:
                result_label.color = (1, 0, 0, 1)  # Red for incorrect
            results_container.add_widget(result_label)

        final_score = (correct_answers * 10) / total_questions
        self.score = f"{final_score:.1f}/10"
        self.ids.score_label.text = f"Điểm của bạn: {self.score}"

    def go_back(self, *args):
        """Returns to the student home screen."""
        self.manager.current = 'student_home'
