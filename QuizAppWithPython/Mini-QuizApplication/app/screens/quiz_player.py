from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty, NumericProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from app.services import quiz_services


class QuizPlayerScreen(Screen):
    quiz_id = StringProperty(None)
    quiz_data = DictProperty({})
    student_answers = DictProperty({})
    current_question_index = NumericProperty(0)

    def on_enter(self, *args):
        """Called when the screen is entered. Loads the quiz data."""
        self.reset_state()
        try:
            self.quiz_data = quiz_services.get_quiz_details(self.quiz_id)
            if not self.quiz_data or not self.quiz_data.get('questions'):
                self._show_popup("Lỗi", "Không thể tải hoặc bài quiz này không có câu hỏi.", self.go_back)
                return
            self.display_current_question()
        except Exception as e:
            self._show_popup("Lỗi", f"Đã xảy ra lỗi: {e}", self.go_back)

    def display_current_question(self):
        """Updates the UI with the current question and its options."""
        container = self.ids.options_container
        container.clear_widgets()

        question_data = self.quiz_data['questions'][self.current_question_index]
        self.ids.question_label.text = question_data['question_title']
        self.ids.quiz_title.text = self.quiz_data['title']
        self.ids.question_counter.text = f"Câu hỏi {self.current_question_index + 1}/{len(self.quiz_data['questions'])}"

        for option in question_data['options']:
            btn = ToggleButton(
                text=option['text'],
                group='answers',
                allow_no_selection=False,
                size_hint_y=None,
                height=40
            )
            container.add_widget(btn)

        if self.current_question_index == len(self.quiz_data['questions']) - 1:
            self.ids.next_button.text = "Nộp bài"
        else:
            self.ids.next_button.text = "Câu tiếp theo"

    def next_question(self):
        """Saves the current answer and moves to the next question or finishes the quiz."""
        # Find selected answer
        selected_answer = None
        for btn in self.ids.options_container.children:
            if btn.state == 'down':
                selected_answer = btn.text
                break
        
        if not selected_answer:
            self._show_popup("Lưu ý", "Bạn cần chọn một đáp án.")
            return

        # Save answer
        question_id = self.quiz_data['questions'][self.current_question_index]['_id']
        self.student_answers[question_id] = selected_answer

        # Move to next question or finish
        if self.current_question_index < len(self.quiz_data['questions']) - 1:
            self.current_question_index += 1
            self.display_current_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        """Calculates the score, saves the result, and shows a summary."""
        correct_answers = 0
        total_questions = len(self.quiz_data['questions'])

        if total_questions == 0:
            self._show_popup("Lỗi", "Không có câu hỏi để chấm điểm.", self.go_back)
            return

        for i, question in enumerate(self.quiz_data['questions']):
            question_id = question['_id']
            correct_answer = question['correct_answer']
            student_answer = self.student_answers.get(question_id)
            if student_answer == correct_answer:
                correct_answers += 1

        # Calculate score on a scale of 10
        final_score = (correct_answers * 10) / total_questions
        final_score_str = f"{final_score:.1f}/10"

        # Save result to DB
        app = App.get_running_app()
        user_id = app.user.get('_id')
        quiz_services.save_quiz_result(user_id, self.quiz_id, final_score_str)

        # Show result popup and go back
        self._show_popup("Hoàn thành!", f"Điểm của bạn là: {final_score_str}", self.go_back)

    def reset_state(self):
        """Resets the screen to its initial state for a new quiz attempt."""
        self.student_answers = {}
        self.current_question_index = 0
        self.ids.options_container.clear_widgets()
        self.ids.question_label.text = ""
        self.ids.quiz_title.text = ""
        self.ids.question_counter.text = ""

    def go_back(self, *args):
        """Returns to the student home screen."""
        self.manager.current = 'student_home'

    def _show_popup(self, title, message, callback=None):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.4))
        if callback:
            popup.bind(on_dismiss=callback)
        popup.open()