from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
from kivy.factory import Factory
from kivy.core.clipboard import Clipboard
from app.services.quiz_services import list_quizzes_by_user, delete_quiz


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
        """Hiển thị danh sách quiz đã tạo với các nút chức năng và giao diện thẻ."""
        quiz_list = self.ids.quiz_list
        quiz_list.clear_widgets()

        try:
            user_id = self.current_user.get("_id")
            if not user_id:
                raise Exception("Không tìm thấy ID người dùng.")

            quizzes = list_quizzes_by_user(user_id)
            if not quizzes:
                quiz_list.add_widget(Label(text="(Chưa có quiz nào được tạo)", color=(1, 1, 1, 0.9), font_size=18))
                return

            for q in quizzes:
                item_layout = Factory.QuizListItem()

                info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
                info_layout.add_widget(
                    Label(
                        text=q['title'], font_size=18, bold=True, halign='left',valign='middle',
                        text_size=(self.width * 0.5, None), color=(1, 1, 1, 1)
                    )
                )
                info_layout.add_widget(
                    Label(
                        text=q.get('description', 'Không có mô tả'), font_size=14,
                        halign='left', valign='middle', text_size=(self.width * 0.5, None),
                        color=(1, 1, 1, 0.8)
                    )
                )
                info_layout.add_widget(
                    Label(
                        text=f"ID: {q['_id']}", font_size=12,
                        halign='left', valign='middle', text_size=(self.width * 0.5, None),
                        color=(1, 1, 1, 0.7)
                    )
                )

                button_layout = BoxLayout(size_hint_x=0.3, spacing=5, orientation='horizontal')
                edit_btn = Button(
                    text="Sửa",
                    background_color=(0, 0, 0, 0),
                    color=(0.6, 0.8, 1, 1),
                    bold=True
                )
                copy_btn = Button(
                    text="Copy ID",
                    background_color=(0, 0, 0, 0),
                    color=(0.7, 1, 0.7, 1), # Greenish color
                    bold=True
                )
                delete_btn = Button(
                    text="Xóa",
                    background_color=(0, 0, 0, 0),
                    color=(1, 0.5, 0.5, 1),
                    bold=True
                )
                
                edit_btn.bind(on_release=partial(self.edit_quiz, q['_id']))
                copy_btn.bind(on_release=partial(self.copy_quiz_id, q['_id']))
                delete_btn.bind(on_release=partial(self.prompt_delete_quiz, q['_id']))

                button_layout.add_widget(edit_btn)
                button_layout.add_widget(copy_btn)
                button_layout.add_widget(delete_btn)

                item_layout.add_widget(info_layout)
                item_layout.add_widget(button_layout)
                quiz_list.add_widget(item_layout)

        except Exception as e:
            quiz_list.add_widget(Label(text=f"Lỗi tải quiz: {e}", color=(1, 0.5, 0.5, 1), font_size=16))

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


    # =========================
    # 🔹 Chuyển sang màn hình tạo quiz
    # =========================
    def go_to_create_quiz(self):
        print("✅ Create Quiz clicked!")
        self.manager.current = "quiz_create"

    def switch_to_tab(self, tab_name):
        """Chuyển đến một tab cụ thể bằng tên và tải nội dung của nó."""
        tab_panel = self.ids.content_tabs
        for tab in tab_panel.tab_list:
            if tab.text == tab_name:
                tab_panel.switch_to(tab)
                if tab_name == "Library":
                    self.load_quiz_library()
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
