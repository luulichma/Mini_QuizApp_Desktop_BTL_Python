from kivy.uix.screenmanager import Screen
from kivy.app import App
from app.services.auth_services import login_user


class LoginScreen(Screen):
    def do_login(self, username, password):
        success, payload = login_user(username, password)
        if success:
            app = App.get_running_app()
            app.user = payload 

            # phân nhánh role
            if payload.get("role") == "student":
                student_home = self.manager.get_screen("student_home")
                student_home.current_user = payload 
                self.manager.current = "student_home"

            elif payload.get("role") == "teacher":
                teacher_home = self.manager.get_screen("teacher_home")
                teacher_home.current_user = payload  
                self.manager.current = "teacher_home"

        else:
            self.ids.status.text = "Sai tài khoản hoặc mật khẩu!"
