from kivy.uix.screenmanager import Screen
from app.services.auth_services import login_user


class LoginScreen(Screen):
    def do_login(self, username, password):
        success, payload = login_user(username, password)
        if success:
            # You might want to store payload in App state later
            self.manager.current = "home"
        else:
            self.ids.status.text = "Sai tài khoản hoặc mật khẩu!"
