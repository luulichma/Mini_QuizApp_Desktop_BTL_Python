from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.factory import Factory
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.clock import Clock
from app.services.quiz_services import get_results_by_user
from app.services import class_services


class StudentHomeScreen(Screen):
    current_user = None

    # ========= utils =========
    def _ensure_container_sizing(self, layout):
        """
        Đảm bảo container hiển thị được trong ScrollView/BoxLayout:
        - Nếu layout có thuộc tính minimum_height: bind nó vào height.
        - Nếu layout bị size_hint_y=None mà height=0 -> đặt height tối thiểu.
        """
        try:
            if hasattr(layout, "minimum_height"):
                # Khi có children, minimum_height sẽ tăng -> auto set vào height
                layout.bind(minimum_height=layout.setter("height"))
            # Nếu không dùng ScrollView thì cũng không hại gì
            if getattr(layout, "size_hint_y", 1) is None and getattr(layout, "height", 0) == 0:
                layout.height = dp(200)
        except Exception as e:
            print("ensure_container sizing warn:", e)

    def _table_height(self, rows_count, rows_visible=10):
        header_h = dp(56)
        row_h = dp(48)
        visible = max(1, min(rows_count, rows_visible))
        return header_h + row_h * visible

    def _add_table(self, layout, column_data, row_data, rows_visible=10, use_pagination=True):
        # clear cũ
        try:
            layout.clear_widgets()
        except Exception as e:
            print("clear_widgets warn:", e)

        # đảm bảo container có height
        self._ensure_container_sizing(layout)

        # ---- HARDCODE HEIGHT RULES ----
        # base heights (hardcoded)
        CLASSES_BASE = dp(700)   # chiều cao mặc định cho danh sách lớp
        HISTORY_BASE = dp(520)   # chiều cao mặc định cho lịch sử quiz

        # chọn base theo layout (so sánh trực tiếp với ids)
        if hasattr(self, "ids") and getattr(self.ids, "my_classes_list", None) is layout:
            table_h = CLASSES_BASE
        elif hasattr(self, "ids") and getattr(self.ids, "history_list", None) is layout:
            table_h = HISTORY_BASE
        else:
            table_h = dp(600)  # fallback

        # nếu dữ liệu nhiều hơn rows_visible thì cho thêm một khoảng để không bị cắt
        if len(row_data) > rows_visible:
            table_h += dp(200)

        # tạo table với chiều cao cố định
        table = MDDataTable(
            size_hint=(1, None),   # QUAN TRỌNG: cố định chiều cao
            height=table_h,        # QUAN TRỌNG: giá trị hardcoded
            use_pagination=use_pagination,
            rows_num=min(rows_visible, max(1, len(row_data))),
            check=False,
            column_data=column_data,
            row_data=row_data,
        )

        print(f"[TABLE] Hardcoded rows={len(row_data)}  height={table_h}  rows_num={table.rows_num}")

        # thêm trên main thread (tránh thêm quá sớm khi on_enter)
        Clock.schedule_once(lambda dt: layout.add_widget(table), 0)

    # ========= lifecycle =========
    def on_enter(self):
        app = App.get_running_app()
        if hasattr(app, "user") and app.user:
            self.current_user = app.user
            self.ids.content_tabs.default_tab = self.ids.home_tab_item
            # KHÔNG nuốt lỗi nữa -> in ra console/popup nếu có
            try:
                self.load_my_classes()
            except Exception as e:
                print("load_my_classes error:", e)
                self._show_popup("Lỗi hiển thị lớp học", str(e))
            try:
                self.load_history()
            except Exception as e:
                print("load_history error:", e)
                self._show_popup("Lỗi hiển thị lịch sử", str(e))
        else:
            print("⚠️ No user found, redirecting to login.")
            self.manager.current = "login"

    # ========= actions =========
    def start_quiz_by_id(self):
        quiz_id = self.ids.id_input.text.strip()
        if not quiz_id:
            self._show_popup("Lỗi", "Vui lòng nhập ID bài quiz.")
            return
        quiz_player_screen = self.manager.get_screen('quiz_player')
        quiz_player_screen.quiz_id = quiz_id
        self.manager.current = 'quiz_player'

    def join_class(self):
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
            self.load_my_classes()

    # ========= data loaders =========
    def load_my_classes(self):
        layout = self.ids.my_classes_list
        layout.clear_widgets()

        if not self.current_user:
            layout.add_widget(Label(text="Vui lòng đăng nhập lại", color=(0,0,0,0.9), font_size=18, size_hint_y=None, height=dp(40)))
            return

        classes = class_services.list_classes_by_student(self.current_user.get("_id"))
        print("classes count:", 0 if classes is None else len(classes))

        if not classes:
            layout.add_widget(Label(text="(Bạn chưa tham gia lớp học nào)", color=(0,0,0,0.9), font_size=18, size_hint_y=None, height=dp(40)))
            return

        column_data = [
            ("Tên lớp", dp(80)),
            ("Mô tả", dp(120)),
            ("Ngày tạo", dp(50))
        ]
        row_data = [
            (c.get('class_name', 'N/A'),
             c.get('description', 'Không có mô tả'),
             c['created_at'].strftime("%d/%m/%Y") if c.get('created_at') else "N/A")
            for c in classes
        ]

        self._add_table(layout, column_data, row_data, rows_visible=10, use_pagination=True)

    def load_history(self):
        layout = self.ids.history_list
        layout.clear_widgets()

        if not self.current_user:
            layout.add_widget(Label(text="Vui lòng đăng nhập lại", color=(0,0,0,0.9), font_size=18, size_hint_y=None, height=dp(40)))
            return

        results = get_results_by_user(self.current_user.get("_id"))
        print("results count:", 0 if results is None else len(results))

        if not results:
            layout.add_widget(Label(text="(Chưa có lịch sử làm bài)", color=(0,0,0,0.9), font_size=18, size_hint_y=None, height=dp(40)))
            return

        column_data = [("Tên Quiz", dp(100)), ("Điểm", dp(50)), ("Ngày làm", dp(50))]
        row_data = [
            (r.get('quiz_title', 'N/A'),
             str(r.get('score', 'N/A')),
             r['submitted_at'].strftime("%d/%m/%Y") if r.get('submitted_at') else "N/A")
            for r in results
        ]

        self._add_table(layout, column_data, row_data, rows_visible=8, use_pagination=True)

    # ========= misc =========
    def go_to_change_password(self):
        self.manager.current = "change_password"

    def logout(self):
        app = App.get_running_app()
        if hasattr(app, 'user'):
            app.user = None
        self.manager.current = "login"

    def _show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()
