from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from app.services import class_services

class ClassCreateScreen(Screen):

    def create_class(self):
        class_name = self.ids.class_name_input.text.strip()
        class_description = self.ids.class_description_input.text.strip()

        if not class_name:
            self._show_popup("Lỗi", "Vui lòng nhập tên lớp học.")
            return

        app = App.get_running_app()
        teacher_id = app.user.get('_id')

        if not teacher_id:
            self._show_popup("Lỗi", "Không tìm thấy thông tin giáo viên. Vui lòng đăng nhập lại.")
            return

        try:
            class_services.create_class(teacher_id, class_name, class_description)
            self._show_popup("Thành công", f"Lớp học '{class_name}' đã được tạo!", self.go_to_class_list)
        except Exception as e:
            self._show_popup("Lỗi", f"Đã xảy ra lỗi khi tạo lớp: {e}")

    def go_to_class_list(self, *args):
        self.clear_inputs()
        teacher_home = self.manager.get_screen("teacher_home")
        teacher_home.switch_to_tab("Classes") # Assuming a 'Classes' tab exists
        self.manager.current = "teacher_home"

    def clear_inputs(self):
        self.ids.class_name_input.text = ""
        self.ids.class_description_input.text = ""

    def go_back(self):
        self.clear_inputs()
        self.manager.current = "teacher_home"

    def _show_popup(self, title, message, on_dismiss_callback=None):
        popup = Popup(title=title, content=Label(text=message, font_size=16), size_hint=(0.6, 0.35))
        if on_dismiss_callback:
            popup.bind(on_dismiss=on_dismiss_callback)
        popup.open()
