from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from app.services.quiz_services import list_quizzes
from kivy.app import App


class StudentHomeScreen(Screen):
    quizzes = ListProperty([])

    def on_pre_enter(self):
        # load quizzes when entering the screen
        try:
            self.quizzes = list_quizzes()
        except Exception as e:
            # if DB error, show empty list
            self.quizzes = []
            print("Error loading quizzes:", e)

    def logout(self):
        app = App.get_running_app()
        app.user = None
        self.manager.current = "login"
