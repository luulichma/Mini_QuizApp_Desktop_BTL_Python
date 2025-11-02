from kivy.uix.screenmanager import Screen
from app.services.auth_services import register_user


class RegisterTeacherScreen(Screen):
    def do_register(self, fullname, dob, id, address, username, password, subject, degree):
        profile = {
            "fullname": fullname,
            "dob": dob,
            "id": id,
            "address": address,
            "subject": subject,
            "degree": degree,
        }
        success, msg = register_user(username, password, "teacher", profile)
        if not success:
            self.ids.status.text = "Tên đăng nhập đã tồn tại!"
            return
        self.ids.status.text = "Đăng ký thành công!"
