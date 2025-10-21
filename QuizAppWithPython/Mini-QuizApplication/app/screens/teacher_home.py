from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from app.services.quiz_services import list_quizzes_by_user


class TeacherHomeScreen(Screen):
    current_tab = "home"
    current_user = None

    def on_enter(self):
        """Khi màn hình được hiển thị"""
        app = App.get_running_app()
        if hasattr(app, "user") and app.user:
            self.current_user = app.user
            self.switch_tab("home")
        else:
            print("⚠️ No user found, redirecting to login.")
            self.manager.current = "login"

    # =========================
    # 🔹 Chuyển giữa các tab
    # =========================
    def switch_tab(self, tab_name):
        """Chuyển tab và cập nhật giao diện"""
        self.current_tab = tab_name

        tabs = {
            "home": self.ids.home_tab,
            "library": self.ids.library_tab,
            "class": self.ids.class_tab,
        }

        # Ẩn tab không hoạt động (opacity=0 và disabled=True)
        for name, tab in tabs.items():
            is_active = (name == tab_name)
            tab.opacity = 1 if is_active else 0
            tab.disabled = not is_active  # ✅ khóa tab không hoạt động

        # Đổi màu nút active trên thanh menu
        for btn_name in ["btn_home", "btn_library", "btn_class"]:
            btn = getattr(self.ids, btn_name)
            btn.background_color = (1, 1, 1, 0.25 if btn.text.lower() == tab_name else 0)

        # Nếu vào tab Library thì load quiz
        if tab_name == "library":
            self.load_quiz_library()

    # =========================
    # 🔹 Load danh sách Quiz
    # =========================
    def load_quiz_library(self):
        """Hiển thị danh sách quiz đã tạo"""
        quiz_list = self.ids.quiz_list
        quiz_list.clear_widgets()

        try:
            quizzes = list_quizzes_by_user(self.current_user["_id"])
            if not quizzes:
                quiz_list.add_widget(
                    Label(
                        text="(Chưa có quiz nào được tạo)",
                        color=(1, 1, 1, 0.9),
                        font_size=18,
                        size_hint_y=None,
                        height=30,
                        halign="center",
                        valign="middle",
                        text_size=(self.width, None)
                    )
                )
                return

            for q in quizzes:
                quiz_list.add_widget(
                    Label(
                        text=f"• {q['title']}",
                        color=(1, 1, 1, 1),
                        font_size=18,
                        size_hint_y=None,
                        height=35,
                        halign="center",
                        valign="middle",
                        text_size=(self.width, None)
                    )
                )
        except Exception as e:
            quiz_list.add_widget(
                Label(
                    text=f"Lỗi tải quiz: {e}",
                    color=(1, 0.5, 0.5, 1),
                    font_size=16,
                    size_hint_y=None,
                    height=30,
                    halign="center",
                )
            )

    # =========================
    # 🔹 Chuyển sang màn hình tạo quiz
    # =========================
    def go_to_create_quiz(self):
        print("✅ Create Quiz clicked!")
        self.manager.current = "quiz_create"

    # =========================
    # 🔹 Menu phụ
    # =========================
    def open_menu(self):
        Popup(
            title="Menu",
            content=Label(text="(Tính năng đang phát triển)"),
            size_hint=(0.5, 0.3),
        ).open()
