from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from app.services import quiz_services

class QuizHistoryScreen(Screen):

    def on_enter(self, *args):
        self.load_quiz_history()

    def load_quiz_history(self):
        app = App.get_running_app()
        user_id = app.user.get('_id')
        if not user_id:
            self.go_back()
            return

        history = quiz_services.get_results_by_user(user_id)
        history_container = self.ids.history_container
        history_container.clear_widgets()

        if not history:
            history_container.add_widget(Label(text="Chưa có lịch sử làm bài.", size_hint_y=None, height=50))
            return

        for item in history:
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=80, padding=10, spacing=5)
            box.add_widget(Label(text=f"Quiz: {item['quiz_title']}", halign='left', size_hint_x=1))
            box.add_widget(Label(text=f"Điểm: {item['score']}", halign='left', size_hint_x=1))
            box.add_widget(Label(text=f"Ngày làm: {item['submitted_at']}", halign='left', size_hint_x=1))
            history_container.add_widget(box)

    def go_back(self, *args):
        self.manager.current = 'student_home'
