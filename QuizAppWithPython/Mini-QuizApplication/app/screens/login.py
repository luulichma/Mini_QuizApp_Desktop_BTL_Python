from kivy.uix.screenmanager import Screen
from kivy.app import App
from app.services.auth_services import login_user


class LoginScreen(Screen):
    def do_login(self, username, password):
        success, payload = login_user(username, password)
        if success:
            app = App.get_running_app()
            # store minimal user info on the App instance for later use
            app.user = payload
            # route based on role
            if payload.get("role") == "student":
                self.manager.current = "student_home"
            else:
                self.manager.current = "home"
        else:
            self.ids.status.text = "Sai tài khoản hoặc mật khẩu!"
