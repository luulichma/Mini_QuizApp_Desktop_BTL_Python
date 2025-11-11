from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.factory import Factory
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from app.services.quiz_services import get_results_by_user
from app.services import class_services


class StudentHomeScreen(Screen):
    current_user = None

    def on_enter(self):
        """Khi màn hình được hiển thị."""
        app = App.get_running_app()
        if hasattr(app, "user") and app.user:
            self.current_user = app.user
            self.ids.content_tabs.default_tab = self.ids.home_tab_item
        else:
            print("⚠️ No user found, redirecting to login.")
            self.manager.current = "login"

    def start_quiz_by_id(self):
        """Lấy ID từ text input và bắt đầu quiz."""
        quiz_id = self.ids.id_input.text.strip()
        if not quiz_id:
            self._show_popup("Lỗi", "Vui lòng nhập ID bài quiz.")
            return

        # Lấy màn hình quiz player và gán ID
        quiz_player_screen = self.manager.get_screen('quiz_player')
        quiz_player_screen.quiz_id = quiz_id

        # Chuyển màn hình
        self.manager.current = 'quiz_player'

    def join_class(self):
        """Tham gia một lớp học bằng ID."""
        class_id = self.ids.id_input.text.strip()
        if not class_id:
            self._show_popup("Lỗi", "Vui lòng nhập ID lớp học.")
            return

        if not self.current_user:
            self._show_popup("Lỗi", "Không tìm thấy thông tin người dùng. Vui lòng đăng nhập lại.")
            return

        student_id = self.current_user.get("_id")
        success, message = class_services.add_student_to_class(class_id, student_id)

        self._show_popup("Thông báo", message)
        if success:
            # Automatically refresh the class list after joining
            self.load_my_classes()

    def load_my_classes(self):
        """Tải và hiển thị danh sách các lớp học mà sinh viên đã tham gia bằng MDDataTable."""
        my_classes_list_layout = self.ids.my_classes_list
        my_classes_list_layout.clear_widgets()

        if not self.current_user:
            my_classes_list_layout.add_widget(Label(text="Vui lòng đăng nhập lại", color=(0, 0, 0, 0.9), font_size=18))
            return

        try:
            user_id = self.current_user.get("_id")
            classes = class_services.list_classes_by_student(user_id)

            if not classes:
                my_classes_list_layout.add_widget(Label(text="(Bạn chưa tham gia lớp học nào)", color=(0, 0, 0, 0.9), font_size=18))
                return

            column_data = [
                ("Tên lớp", dp(80)),
                ("Mô tả", dp(120)),
                ("Ngày tạo", dp(50)),
            ]

            row_data = []
            for cls in classes:
                created_at_str = cls['created_at'].strftime("%d/%m/%Y") if cls.get('created_at') else "N/A"
                row_data.append((cls['class_name'], cls.get('description', 'Không có mô tả'), created_at_str))

            data_table = MDDataTable(
                size_hint=(1, 1),  # ← FIX: Auto-fill parent
                use_pagination=True,
                rows_num=8,
                check=False,
                column_data=column_data,
                row_data=row_data,
            )
            # ✅ FIX: Không set height cố định
            my_classes_list_layout.add_widget(data_table)

        except Exception as e:
            my_classes_list_layout.add_widget(Label(text=f"Lỗi tải danh sách lớp học: {e}", color=(1, 0, 0, 1)))

    def load_history(self):
        """Tải và hiển thị lịch sử các bài đã làm bằng MDDataTable."""
        history_list_layout = self.ids.history_list
        history_list_layout.clear_widgets()

        if not self.current_user:
            history_list_layout.add_widget(Label(text="Vui lòng đăng nhập lại", color=(0, 0, 0, 0.9), font_size=18))
            return

        try:
            user_id = self.current_user.get("_id")
            results = get_results_by_user(user_id)

            if not results:
                history_list_layout.add_widget(Label(text="(Chưa có lịch sử làm bài)", color=(0, 0, 0, 0.9), font_size=18))
                return

            column_data = [
                ("Tên Quiz", dp(100)),
                ("Điểm", dp(50)),
                ("Ngày làm", dp(50)),
            ]

            row_data = []
            for res in results:
                submitted_date = res['submitted_at'].strftime("%d/%m/%Y") if res.get('submitted_at') else "N/A"
                row_data.append((res['quiz_title'], res['score'], submitted_date))

            data_table = MDDataTable(
                size_hint=(1, 1),  # ← FIX: Auto-fill parent
                use_pagination=True,
                rows_num=8,
                check=False,
                column_data=column_data,
                row_data=row_data,
            )
            # ✅ FIX: Không set height cố định
            history_list_layout.add_widget(data_table)

        except Exception as e:
            history_list_layout.add_widget(Label(text=f"Lỗi tải lịch sử: {e}", color=(1, 0, 0, 1)))

    def go_to_change_password(self):
        self.manager.current = "change_password"

    def logout(self):
        """Đăng xuất và quay về màn hình đăng nhập."""
        app = App.get_running_app()
        if hasattr(app, 'user'):
            app.user = None
        self.manager.current = "login"

    def _show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()