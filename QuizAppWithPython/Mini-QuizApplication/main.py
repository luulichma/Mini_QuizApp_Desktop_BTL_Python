from kivy.core.window import Window
Window.maximize()

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# Import các screen
from app.screens.login import LoginScreen
from app.screens.register import RegisterScreen
from app.screens.register_teacher import RegisterTeacherScreen
from app.screens.register_student import RegisterStudentScreen
from app.screens.home import HomeScreen
from app.screens.student_home import StudentHomeScreen
from app.screens.teacher_home import TeacherHomeScreen
from app.screens.quiz_create import QuizCreateScreen
from app.screens.quiz_player import QuizPlayerScreen
from app.screens.change_password import ChangePasswordScreen
from app.screens.result import ResultScreen

from app.screens.class_create import ClassCreateScreen
from app.screens.class_details import ClassDetailsScreen

class QuizApp(App):
    def build(self):
        # Load tất cả file KV
        Builder.load_file("app/kv/login.kv")
        Builder.load_file("app/kv/register.kv")
        Builder.load_file("app/kv/register_teacher.kv")
        Builder.load_file("app/kv/register_student.kv")
        Builder.load_file("app/kv/student_home.kv")
        Builder.load_file("app/kv/teacher_home.kv")
        Builder.load_file("app/kv/quiz_create.kv")
        Builder.load_file("app/kv/quiz_player.kv")
        Builder.load_file("app/kv/change_password.kv")
        Builder.load_file("app/kv/result.kv")
        Builder.load_file("app/kv/class_create.kv")
        Builder.load_file("app/kv/class_details.kv")

        # Tạo ScreenManager và thêm các màn hình
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(RegisterTeacherScreen(name="register_teacher"))
        sm.add_widget(RegisterStudentScreen(name="register_student"))
        sm.add_widget(StudentHomeScreen(name="student_home"))
        sm.add_widget(TeacherHomeScreen(name="teacher_home"))
        sm.add_widget(QuizCreateScreen(name="quiz_create"))
        sm.add_widget(QuizPlayerScreen(name="quiz_player"))
        sm.add_widget(ChangePasswordScreen(name="change_password"))
        sm.add_widget(ResultScreen(name="result_screen"))
        sm.add_widget(ClassCreateScreen(name="class_create"))
        sm.add_widget(ClassDetailsScreen(name="class_details"))
        sm.add_widget(HomeScreen(name="home"))

        return sm


if __name__ == "__main__":
    QuizApp().run()
