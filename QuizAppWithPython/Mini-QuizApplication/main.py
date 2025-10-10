from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# import các screen
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.register_teacher import RegisterTeacherScreen
from screens.register_student import RegisterStudentScreen
from screens.home import HomeScreen

class QuizApp(App):
    def build(self):
        # Load tất cả file .kv
        Builder.load_file("kv/login.kv")
        Builder.load_file("kv/register.kv")
        Builder.load_file("kv/register_teacher.kv")
        Builder.load_file("kv/register_student.kv")
        Builder.load_file("kv/home.kv")

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(RegisterTeacherScreen(name="register_teacher"))
        sm.add_widget(RegisterStudentScreen(name="register_student"))
        sm.add_widget(HomeScreen(name="home"))
        return sm

if __name__ == "__main__":
    QuizApp().run()
