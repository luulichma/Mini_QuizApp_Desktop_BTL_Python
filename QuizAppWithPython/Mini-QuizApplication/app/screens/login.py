from kivy.uix.screenmanager import Screen
from utils.storage import load_users

class LoginScreen(Screen):
    def do_login(self, username, password):
        users = load_users()
        if username in users and users[username]["password"] == password:
            self.manager.current = "home"
        else:
            self.ids.status.text = "Sai tài khoản hoặc mật khẩu!"
