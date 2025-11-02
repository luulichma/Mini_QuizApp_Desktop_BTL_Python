from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line, RoundedRectangle
from app.services import quiz_services
from app.services.quiz_services import get_quiz_details, update_quiz


class QuizCreateScreen(Screen):
    editing_quiz_id = None

    # ===================== STYLE HELPER =====================
    def style_textinput(self, widget):
        """Thêm viền xám nhạt + hiệu ứng focus xanh."""
        def update_border(*_):
            widget.canvas.before.clear()
            with widget.canvas.before:
                if widget.focus:
                    Color(0.25, 0.5, 1, 1)  # xanh khi focus
                else:
                    Color(0.85, 0.85, 0.85, 1)  # xám khi blur
                Line(rounded_rectangle=[widget.x, widget.y, widget.width, widget.height, 8], width=1.2)
        widget.bind(pos=update_border, size=update_border, focus=update_border)
        update_border()

    # ===================== LOAD QUIZ =====================
    def load_quiz_for_editing(self, quiz_id):
        self.editing_quiz_id = quiz_id
        quiz_data = get_quiz_details(quiz_id)
        if not quiz_data:
            self._popup("Lỗi", "Không thể tải dữ liệu quiz.")
            self.cancel_editing()
            return

        self.ids.screen_title.text = "Sửa Quiz"
        self.ids.quiz_name.text = quiz_data.get("title", "")
        self.ids.quiz_description.text = quiz_data.get("description", "")
        self.children[0].children[0].children[0].text = "Cập nhật Quiz"

        container = self.ids.question_container
        container.clear_widgets()
        for question in quiz_data.get("questions", []):
            self.add_question_block_with_data(question)

    # ===================== CÂU HỎI CÓ DỮ LIỆU =====================
    def add_question_block_with_data(self, question_data):
        container = self.ids.question_container
        question_box = BoxLayout(orientation="vertical", size_hint_y=None, height=350, spacing=10)
        question_box.question_index = len(container.children) + 1
        question_box.radio_group = f"group_{question_box.question_index}"

        # Ô nhập câu hỏi
        q_input = TextInput(
            text=question_data.get("question_title", ""),
            size_hint_y=None, height=60,
            background_normal="", background_active="",
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
            font_size=16, padding=[10, 8],
            cursor_color=(0.23, 0.51, 0.96, 1),
        )
        self.style_textinput(q_input)
        question_box.add_widget(q_input)

        # ScrollView chứa danh sách đáp án
        scroll_area = ScrollView(size_hint_y=None, height=200, do_scroll_x=False, bar_width=0)
        options_box = GridLayout(cols=1, spacing=5, size_hint_y=None)
        options_box.bind(minimum_height=options_box.setter("height"))
        scroll_area.add_widget(options_box)
        question_box.add_widget(scroll_area)
        question_box.options_box = options_box

        # Thêm các đáp án đã có
        for option in question_data.get("options", []):
            self._add_option_field_with_data(options_box, question_box.radio_group, option, question_data.get("correct_answer"))

        # Nút Thêm/Xóa đáp án
        control_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        add_btn = Button(text="Thêm đáp án", background_color=(0.96, 0.96, 0.96, 1), color=(0.15, 0.15, 0.15, 1))
        remove_btn = Button(text="Xóa đáp án cuối", background_color=(0.96, 0.96, 0.96, 1), color=(0.15, 0.15, 0.15, 1))
        add_btn.bind(on_release=lambda *_: self._add_option_field(options_box, question_box.radio_group))
        remove_btn.bind(on_release=lambda *_: self._remove_option_field(options_box))
        control_box.add_widget(add_btn)
        control_box.add_widget(remove_btn)
        question_box.add_widget(control_box)

        container.add_widget(question_box)

    # ===================== CÂU HỎI MỚI =====================
    def add_question_block(self):
        container = self.ids.question_container
        question_box = BoxLayout(orientation="vertical", size_hint_y=None, height=350, spacing=10)
        question_box.question_index = len(container.children) + 1
        question_box.radio_group = f"group_{question_box.question_index}"

        # Ô nhập câu hỏi
        q_input = TextInput(
            hint_text=f"Câu hỏi {question_box.question_index}",
            size_hint_y=None, height=60,
            background_normal="", background_active="",
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
            font_size=16, padding=[10, 8],
            cursor_color=(0.23, 0.51, 0.96, 1),
        )
        self.style_textinput(q_input)
        question_box.add_widget(q_input)

        # ScrollView chứa danh sách đáp án
        scroll_area = ScrollView(size_hint_y=None, height=200, do_scroll_x=False, bar_width=0)
        options_box = GridLayout(cols=1, spacing=5, size_hint_y=None)
        options_box.bind(minimum_height=options_box.setter("height"))
        scroll_area.add_widget(options_box)
        question_box.add_widget(scroll_area)
        question_box.options_box = options_box

        # Thêm 2 đáp án mặc định
        for _ in range(2):
            self._add_option_field(options_box, question_box.radio_group)

        # Nút Thêm/Xóa đáp án
        control_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        add_btn = Button(text="Thêm đáp án", background_color=(0.96, 0.96, 0.96, 1), color=(0.15, 0.15, 0.15, 1))
        remove_btn = Button(text="Xóa đáp án cuối", background_color=(0.96, 0.96, 0.96, 1), color=(0.15, 0.15, 0.15, 1))
        add_btn.bind(on_release=lambda *_: self._add_option_field(options_box, question_box.radio_group))
        remove_btn.bind(on_release=lambda *_: self._remove_option_field(options_box))
        control_box.add_widget(add_btn)
        control_box.add_widget(remove_btn)
        question_box.add_widget(control_box)

        container.add_widget(question_box)

        # ===================== THÊM ĐÁP ÁN =====================
    def _add_option_field(self, parent_box, radio_group):
        line = BoxLayout(orientation="horizontal", size_hint_y=None, height=45, spacing=10, padding=[5, 0])

        # ToggleButton — chọn đáp án đúng
        rb = ToggleButton(
            group=radio_group,
            text="✓",                # ký hiệu tích ✅
            font_size=18,
            size_hint_x=0.12,
            background_normal="",
            background_down="",
            background_color=(0.9, 0.9, 0.9, 1),
            color=(0.3, 0.3, 0.3, 1),
            allow_no_selection=False
        )

        # Cập nhật màu toggle theo trạng thái
        rb.bind(state=lambda instance, val: self._update_toggle_color(instance, val))
        self._update_toggle_color(rb, rb.state)

        # Ô nhập văn bản đáp án
        txt = TextInput(
            hint_text=f"Đáp án {len(parent_box.children) + 1}",
            size_hint_x=0.88,
            background_normal="",
            background_active="",
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
            font_size=16,
            padding=[10, 8],
            cursor_color=(0.23, 0.51, 0.96, 1),
        )
        self.style_textinput(txt)

        # Gắn 2 widget vào dòng
        line.add_widget(rb)
        line.add_widget(txt)
        parent_box.add_widget(line)


    # ===================== HIỂN THỊ MÀU CHO TOGGLE =====================
    def _update_toggle_color(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            # bo tròn nút toggle
            if value == "down":
                Color(0.23, 0.51, 0.96, 1)  # xanh khi chọn
            else:
                Color(0.85, 0.85, 0.85, 1)  # xám khi chưa chọn
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[8])
        instance.bind(
            pos=lambda *_: self._update_toggle_color(instance, instance.state),
            size=lambda *_: self._update_toggle_color(instance, instance.state)
        )


    # ===================== XÓA ĐÁP ÁN =====================
    def _remove_option_field(self, parent_box):
        if parent_box.children:
            parent_box.remove_widget(parent_box.children[0])

    # ===================== SAVE QUIZ =====================
    def save_quiz(self):
        quiz_name = self.ids.quiz_name.text.strip()
        quiz_description = self.ids.quiz_description.text.strip()
        if not quiz_name:
            self._popup("Lỗi", "Vui lòng nhập tên Quiz!")
            return

        container = self.ids.question_container
        if not container.children:
            self._popup("Lỗi", "Quiz cần ít nhất 1 câu hỏi!")
            return

        questions_data = []
        for q_box in reversed(container.children):
            q_input = q_box.children[-1]
            q_text = q_input.text.strip()
            if not q_text:
                continue

            options_box = q_box.options_box
            options = []
            correct_answer = None

            for line in reversed(options_box.children):
                txt, rb = line.children
                val = txt.text.strip()
                if val:
                    if val in [opt["text"] for opt in options]:
                        self._popup("Lỗi", f"Đáp án bị trùng trong câu hỏi: {q_text}")
                        return
                    options.append({"text": val, "display_order": len(options) + 1})
                    if rb.state == "down":
                        correct_answer = val

            if not correct_answer:
                self._popup("Lỗi", f"Câu hỏi '{q_text}' chưa chọn đáp án đúng!")
                return

            questions_data.append({
                "question_title": q_text,
                "correct_answer": correct_answer,
                "options": options,
            })

        if not questions_data:
            self._popup("Lỗi", "Không có câu hỏi hợp lệ nào.")
            return

        if self.editing_quiz_id:
            update_quiz(self.editing_quiz_id, quiz_name, quiz_description, questions_data)
            self._popup("Thành công", f"Quiz '{quiz_name}' đã được cập nhật!", self.go_to_library)
        else:
            from kivy.app import App
            app = App.get_running_app()
            user_id = app.user.get("_id") if hasattr(app, "user") and app.user else None
            if not user_id:
                self._popup("Lỗi", "Không tìm thấy thông tin người dùng. Vui lòng đăng nhập lại.")
                return

            quiz_id = quiz_services.create_quiz(
                user_id=user_id, title=quiz_name, description=quiz_description
            )
            for q_data in questions_data:
                quiz_services.add_question(quiz_id, q_data["question_title"], q_data["correct_answer"], q_data["options"])
            self._popup("Thành công", f"Quiz '{quiz_name}' đã được tạo!", self.go_to_library)

    # ===================== NAVIGATION =====================
    def go_to_library(self, *args):
        self.clear_inputs()
        teacher_home = self.manager.get_screen("teacher_home")
        teacher_home.switch_to_tab("Library")
        self.manager.current = "teacher_home"

    def clear_inputs(self):
        self.ids.quiz_name.text = ""
        self.ids.quiz_description.text = ""
        self.ids.question_container.clear_widgets()
        self.add_question_block()

    def _popup(self, title, msg, on_dismiss_callback=None):
        popup = Popup(title=title, content=Label(text=msg, font_size=16), size_hint=(0.6, 0.35))
        if on_dismiss_callback:
            popup.bind(on_dismiss=on_dismiss_callback)
        popup.open()

    def go_back(self):
        self.cancel_editing()
        self.manager.current = "teacher_home"

    def cancel_editing(self):
        self.editing_quiz_id = None
        self.ids.screen_title.text = "Tạo Quiz"
        self.clear_inputs()
        self.children[0].children[0].children[0].text = "Tạo Quiz"
