from kivy.uix.screenmanager import Screen
from utils.storage import load_users, save_users

class RegisterTeacherScreen(Screen):
    def do_register(self, fullname, dob, address, username, password, subject, degree):
        users = load_users()
        if username in users:
            self.ids.status.text = "Tên đăng nhập đã tồn tại!"
            return
        users[username] = {
            "password": password,
            "role": "teacher",
            "fullname": fullname,
            "dob": dob,
            "address": address,
            "subject": subject,
            "degree": degree
        }
        save_users(users)
        self.ids.status.text = "Đăng ký thành công!"
