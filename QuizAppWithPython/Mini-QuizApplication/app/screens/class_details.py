from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.clipboard import Clipboard
from app.services import class_services
from app.services import auth_services

class ClassDetailsScreen(Screen):
    class_id = None

    def on_enter(self, *args):
        if self.class_id:
            self.load_class_details()
        else:
            self.go_back()

    def load_class_details(self):
        class_data = class_services.get_class_details(self.class_id)
        if class_data:
            self.ids.class_name_label.text = f"Lớp: {class_data['class_name']}"
            self.ids.class_description_label.text = f"Mô tả: {class_data.get('description', 'Không có')}"
            self.ids.class_id_label.text = f"ID: {self.class_id}"
            self.load_students_in_class()
        else:
            self._show_popup("Lỗi", "Không tìm thấy thông tin lớp học.", self.go_back)

    def copy_class_id(self):
        Clipboard.copy(self.class_id)
        self._show_popup("Thành công", "Đã sao chép ID lớp học vào clipboard.")

    def load_students_in_class(self):
        students_container = self.ids.students_container
        students_container.clear_widgets()

        students = class_services.list_students_in_class(self.class_id)

        if not students:
            students_container.add_widget(Label(text="Chưa có học sinh nào trong lớp.", size_hint_y=None, height=50))
            return

        for student in students:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=5, spacing=5)
            box.add_widget(Label(text=f"{student['name']} ({student['username']})"))
            remove_button = Button(text="Xóa", size_hint_x=0.2)
            remove_button.bind(on_release=lambda btn, s_id=student['_id']: self.remove_student(s_id))
            box.add_widget(remove_button)
            students_container.add_widget(box)

    def add_student(self):
        student_id = self.ids.student_id_input.text.strip()
        if not student_id:
            self._show_popup("Lỗi", "Vui lòng nhập mã sinh viên.")
            return
        
        # Check if student exists and is a player
        user = auth_services.get_user_by_student_id(student_id)
        if not user or user['role'] != 'player':
            self._show_popup("Lỗi", "Không tìm thấy học sinh hoặc người dùng không phải là học sinh.")
            return

        if class_services.add_student_to_class(self.class_id, str(user['_id'])):
            self._show_popup("Thành công", f"Đã thêm học sinh {user['username']} vào lớp.")
            self.ids.student_id_input.text = ""
            self.load_students_in_class()
        else:
            self._show_popup("Lỗi", f"Không thể thêm học sinh. Có thể học sinh đã có trong lớp.")

    def remove_student(self, student_id):
        if class_services.remove_student_from_class(self.class_id, student_id):
            self._show_popup("Thành công", "Đã xóa học sinh khỏi lớp.")
            self.load_students_in_class()
        else:
            self._show_popup("Lỗi", "Không thể xóa học sinh khỏi lớp.")

    def delete_class(self):
        def confirm_delete(instance):
            if instance.text == 'Yes':
                if class_services.delete_class(self.class_id):
                    self._show_popup("Thành công", "Đã xóa lớp học.", self.go_to_class_list)
                else:
                    self._show_popup("Lỗi", "Không thể xóa lớp học.")
            popup.dismiss()

        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text="Bạn có chắc chắn muốn xóa lớp học này?", size_hint_y=None, height=40))
        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        yes_btn = Button(text='Yes')
        no_btn = Button(text='No')
        yes_btn.bind(on_release=confirm_delete)
        no_btn.bind(on_release=confirm_delete)
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)

        popup = Popup(title="Xác nhận xóa", content=content, size_hint=(0.7, 0.4))
        popup.open()

    def go_to_class_list(self, *args):
        teacher_screen = self.manager.get_screen('teacher_home')
        # The 'Lớp học' tab is the 3rd tab, index 2
        teacher_screen.ids.content_tabs.switch_to(teacher_screen.ids.content_tabs.tab_list[2])
        self.manager.current = 'teacher_home'

    def go_back(self, *args):
        self.manager.current = 'teacher_home'

    def _show_popup(self, title, message, on_dismiss_callback=None):
        popup = Popup(title=title, content=Label(text=message, font_size=16), size_hint=(0.6, 0.35))
        if on_dismiss_callback:
            popup.bind(on_dismiss=on_dismiss_callback)
        popup.open()
