from kivy.uix.screenmanager import Screen
from app.services.auth_services import register_user
from kivy.app import App


class RegisterStudentScreen(Screen):
    def do_register(self, fullname, dob, id, address, username, password, class_name, major):
        profile = {
            "fullname": fullname,
            "dob": dob,
            "id": id,
            "address": address,
            "class": class_name,
            "major": major,
        }
        success, msg = register_user(username, password, "student", profile)
        if not success:
            self.ids.status.text = "Tên đăng nhập đã tồn tại!"
            return
        self.ids.status.text = "Đăng ký thành công!"

    def go_back(self):
        app = App.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'register'
