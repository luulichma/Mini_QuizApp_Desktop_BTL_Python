from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
from kivy.factory import Factory
from kivy.core.clipboard import Clipboard
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from app.services.quiz_services import list_quizzes_by_user, delete_quiz
from app.services import class_services


class TeacherHomeScreen(Screen):
    current_user = None

    def on_enter(self):
        """Khi màn hình được hiển thị"""
        # Gán tab Home làm tab mặc định một cách tường minh
        self.ids.content_tabs.default_tab = self.ids.home_tab_item

        app = App.get_running_app()
        if hasattr(app, "user") and app.user:
            self.current_user = app.user
        else:
            print("⚠️ No user found, redirecting to login.")
            self.manager.current = "login"

    # =========================
    # 🔹 Load danh sách Quiz
    # =========================
    def load_quiz_library(self):
        """Hiển thị danh sách quiz đã tạo với MDDataTable."""
        quiz_list_layout = self.ids.quiz_list
        quiz_list_layout.clear_widgets()

        try:
            user_id = self.current_user.get("_id")
            if not user_id:
                raise Exception("Không tìm thấy ID người dùng.")

            quizzes = list_quizzes_by_user(user_id)
            if not quizzes:
                quiz_list_layout.add_widget(Label(text="(Chưa có quiz nào được tạo)", color=(0, 0, 0, 0.9), font_size=18))
                return

            column_data = [
                ("ID Quiz", dp(80)),
                ("Tên Quiz", dp(60)),
                ("Mô tả", dp(100)),
            ]

            row_data = [
                (
                    q['_id'], 
                    q['title'], 
                    q.get('description', 'Không có mô tả'),
                ) for q in quizzes
            ]

            data_table = MDDataTable(
                size_hint=(1, 1),
                use_pagination=True,  
                rows_num=10,
                check=False,
                column_data=column_data,
                row_data=row_data,
            )
            # ✅ FIX: Không set height cố định khi dùng pagination
            data_table.bind(on_row_press=self.on_quiz_row_press)
            quiz_list_layout.add_widget(data_table)

        except Exception as e:
            quiz_list_layout.add_widget(Label(text=f"Lỗi tải quiz: {e}", color=(1, 0, 0, 1), font_size=16))

    def on_quiz_row_press(self, instance_table, instance_row):
        """
        Khi một hàng được nhấn, hiển thị một Popup với các tùy chọn hành động.
        """
        # Lấy quiz_id từ dữ liệu hàng. Dùng try-except để phòng trường hợp lỗi.
        try:
            num_cols = len(instance_table.column_data)  # 3
            row_num = instance_row.index // num_cols   # Tính row thực
            quiz_id = instance_table.row_data[row_num][0]
        except IndexError:
            print(f"Lỗi: Không thể lấy quiz_id cho hàng có index {instance_row.index}")
            return

        # Tạo nội dung cho Popup
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Tạo các nút hành động
        edit_btn = Button(text='Sửa Quiz', size_hint_y=None, height=dp(40))
        copy_btn = Button(text='Copy ID', size_hint_y=None, height=dp(40))
        delete_btn = Button(text='Xóa Quiz', size_hint_y=None, height=dp(40), background_color=(1, 0.2, 0.2, 1))

        content.add_widget(edit_btn)
        content.add_widget(copy_btn)
        content.add_widget(delete_btn)

        # Tạo Popup
        popup = Popup(title=f"Hành động cho Quiz ID:\n{quiz_id}",
                      content=content,
                      size_hint=(0.5, 0.4))

        # Gán hành động cho các nút (sử dụng partial để truyền tham số)
        edit_btn.bind(on_release=lambda *_: self.edit_quiz(quiz_id))
        copy_btn.bind(on_release=lambda *_: self.copy_quiz_id(quiz_id))
        delete_btn.bind(on_release=lambda *_: self.prompt_delete_quiz(quiz_id))

        # Đóng popup sau khi một hành động được chọn
        edit_btn.bind(on_release=popup.dismiss)
        copy_btn.bind(on_release=popup.dismiss)
        delete_btn.bind(on_release=popup.dismiss)
        
        popup.open()


    def copy_quiz_id(self, quiz_id, *args):
        """Copies the quiz ID to the clipboard and shows a confirmation popup."""
        Clipboard.copy(quiz_id)
        popup = Popup(title="Thông báo",
                      content=Label(text="Đã sao chép ID vào clipboard!"),
                      size_hint=(0.4, 0.2))
        popup.open()

    def prompt_delete_quiz(self, quiz_id, *args):
        """Hiển thị popup xác nhận xóa."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text='Bạn có chắc chắn muốn xóa quiz này không?\nHành động này không thể hoàn tác.'))
        
        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        yes_btn = Button(text='Có, Xóa')
        no_btn = Button(text='Không')
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)

        popup = Popup(title='Xác nhận Xóa', content=content, size_hint=(0.6, 0.4))

        # Gán hàm xử lý khi nhấn nút
        yes_btn.bind(on_release=lambda *_: self.confirm_delete_quiz(quiz_id, popup))
        no_btn.bind(on_release=popup.dismiss)
        
        popup.open()

    def confirm_delete_quiz(self, quiz_id, popup, *args):
        """Thực hiện xóa và làm mới danh sách."""
        popup.dismiss()
        try:
            deleted_count = delete_quiz(quiz_id)
            if deleted_count > 0:
                # Làm mới lại danh sách quiz
                self.load_quiz_library()
            else:
                # Hiển thị lỗi nếu không xóa được
                error_popup = Popup(title='Lỗi', content=Label(text='Không tìm thấy quiz để xóa.'), size_hint=(0.5, 0.3))
                error_popup.open()
        except Exception as e:
            error_popup = Popup(title='Lỗi', content=Label(text=f'Đã xảy ra lỗi: {e}'), size_hint=(0.5, 0.3))
            error_popup.open()

    def edit_quiz(self, quiz_id, *args):
        """Chuyển sang màn hình sửa quiz và tải dữ liệu."""
        create_screen = self.manager.get_screen('quiz_create')
        create_screen.load_quiz_for_editing(quiz_id)
        self.manager.current = 'quiz_create'

    def load_classes(self):
        class_list_layout = self.ids.class_list
        class_list_layout.clear_widgets()

        if not self.current_user:
            class_list_layout.add_widget(Label(text="Vui lòng đăng nhập lại", color=(0, 0, 0, 0.9), font_size=18))
            return

        try:
            user_id = self.current_user.get("_id")
            classes = class_services.list_classes_by_teacher(user_id)

            if not classes:
                class_list_layout.add_widget(Label(text="(Chưa có lớp học nào)", color=(0, 0, 0, 0.9), font_size=18))
                return

            # Prepare data for MDDataTable
            column_data = [
                ("ID Lớp học", dp(100)),
                ("Tên lớp", dp(80)),
                ("Mô tả", dp(120)),
                ("Ngày tạo", dp(60)),
                ("Thao tác", dp(30))
            ]
            row_data = []
            for cls in classes:
                # Format created_at for display
                created_at_str = cls['created_at'].strftime("%d/%m/%Y") if cls.get('created_at') else "N/A"
                row_data.append(
                    (
                        cls['_id'],
                        cls['class_name'],
                        cls.get('description', 'Không có mô tả'),
                        created_at_str,
                        "Chi tiết" # Action for details
                    )
                )
            
            # Create MDDataTable
            data_table = MDDataTable(
                size_hint=(1, 1),  # ← FIX: Change to (1, 1) for auto-fill
                use_pagination=True,
                rows_num=8,  # ← Show 8 rows per page
                check=False,
                column_data=column_data,
                row_data=row_data,
            )
            # ✅ FIX: Không set height cố định khi dùng pagination
            # Bind on_row_press to handle "Chi tiết" button click
            data_table.bind(on_row_press=self.on_class_row_press)
            
            class_list_layout.add_widget(data_table)

        except Exception as e:
            class_list_layout.add_widget(Label(text=f"Lỗi tải lớp học: {e}", color=(1, 0, 0, 1)))

    def on_class_row_press(self, instance_table, instance_row):
        """Handles row press event for the class data table."""
        num_cols = len(instance_table.column_data)
        row_num = instance_row.index // num_cols
        class_id = instance_table.row_data[row_num][0]
        self.go_to_class_details(class_id)

    def go_to_class_details(self, class_id, *args):
        details_screen = self.manager.get_screen('class_details')
        details_screen.class_id = class_id
        self.manager.current = 'class_details'

    # =========================
    # 🔹 Chuyển sang màn hình tạo quiz
    # =========================
    def go_to_create_quiz(self):
        print("✅ Create Quiz clicked!")
        self.manager.current = "quiz_create"

    def go_to_create_class(self):
        self.manager.current = "class_create"

    def switch_to_tab(self, tab_name):
        """Chuyển đến một tab cụ thể bằng tên và tải nội dung của nó."""
        tab_panel = self.ids.content_tabs
        for tab in tab_panel.tab_list:
            if tab.text == tab_name:
                tab_panel.switch_to(tab)
                if tab_name == "Library":
                    self.load_quiz_library()
                elif tab_name == "Lớp học":
                    self.load_classes()
                break

    def go_to_change_password(self):
        self.manager.current = "change_password"

    # =========================
    # 🔹 Menu phụ
    # =========================
    def logout(self):
        """Đăng xuất và quay về màn hình đăng nhập."""
        app = App.get_running_app()
        if hasattr(app, 'user'):
            app.user = None
        self.manager.current = "login"
