from kivy.uix.screenmanager import Screen
from utils.storage import load_users, save_users

class RegisterStudentScreen(Screen):
    def do_register(self, fullname, dob, address, username, password, class_name, major):
        users = load_users()
        if username in users:
            self.ids.status.text = "Tên đăng nhập đã tồn tại!"
            return
        users[username] = {
            "password": password,
            "role": "student",
            "fullname": fullname,
            "dob": dob,
            "address": address,
            "class": class_name,
            "major": major
        }
        save_users(users)
        self.ids.status.text = "Đăng ký thành công!"
