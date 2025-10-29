from kivy.uix.screenmanager import Screen
from kivy.app import App
from app.services.auth_services import change_password

class ChangePasswordScreen(Screen):
    def save_password(self):
        old_password = self.ids.old_password.text
        new_password = self.ids.new_password.text
        confirm_new_password = self.ids.confirm_new_password.text
        status_label = self.ids.status_label

        if not all([old_password, new_password, confirm_new_password]):
            status_label.text = "Vui lòng điền đầy đủ thông tin."
            return

        if new_password != confirm_new_password:
            status_label.text = "Mật khẩu mới không khớp."
            return

        app = App.get_running_app()
        user_id = app.user.get("_id")

        success, message = change_password(user_id, old_password, new_password)

        status_label.text = message
        if success:
            self.clear_fields()

    def go_back(self):
        self.clear_fields()
        # Determine the previous screen based on user role
        app = App.get_running_app()
        role = app.user.get("role")
        if role == "student":
            self.manager.current = "student_home"
        elif role == "teacher":
            self.manager.current = "teacher_home"
        else:
            self.manager.current = "login" # Fallback

    def clear_fields(self):
        self.ids.old_password.text = ""
        self.ids.new_password.text = ""
        self.ids.confirm_new_password.text = ""
        self.ids.status_label.text = ""
