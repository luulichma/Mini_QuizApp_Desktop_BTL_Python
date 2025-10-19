from kivy.uix.screenmanager import Screen
from app.services.auth_services import register_user


class RegisterStudentScreen(Screen):
    def do_register(self, fullname, dob, address, username, password, class_name, major):
        profile = {
            "fullname": fullname,
            "dob": dob,
            "address": address,
            "class": class_name,
            "major": major,
        }
        success, msg = register_user(username, password, "student", profile)
        if not success:
            self.ids.status.text = "Tên đăng nhập đã tồn tại!"
            return
        self.ids.status.text = "Đăng ký thành công!"
