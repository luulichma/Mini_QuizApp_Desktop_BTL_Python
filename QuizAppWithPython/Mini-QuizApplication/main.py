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

        # Tạo ScreenManager và thêm các màn hình
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(RegisterTeacherScreen(name="register_teacher"))
        sm.add_widget(RegisterStudentScreen(name="register_student"))
        sm.add_widget(StudentHomeScreen(name="student_home"))
        sm.add_widget(TeacherHomeScreen(name="teacher_home"))
        sm.add_widget(QuizCreateScreen(name="quiz_create")) 
        sm.add_widget(HomeScreen(name="home"))

        return sm


if __name__ == "__main__":
    QuizApp().run()
