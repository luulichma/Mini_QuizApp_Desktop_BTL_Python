from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from app.services import quiz_services


class QuizCreateScreen(Screen):
    def on_enter(self):
        container = self.ids.question_container
        if not container.children:
            self.add_question_block()

    def add_question_block(self):
        """Tạo một khối câu hỏi gồm TextInput + danh sách đáp án"""
        container = self.ids.question_container

        question_box = BoxLayout(orientation="vertical", size_hint_y=None, height=300, spacing=10)
        question_box.question_index = len(container.children) + 1
        question_box.radio_group = f"group_{question_box.question_index}"

        # Tiêu đề câu hỏi
        q_input = TextInput(
            hint_text=f"Câu hỏi {question_box.question_index}",
            size_hint_y=None,
            height=60,
            background_color=(1, 1, 1, 0.25),
            foreground_color=(1, 1, 1, 1),
            font_size=16,
            padding=[10, 8],
        )
        question_box.add_widget(q_input)

        # Danh sách đáp án
        options_box = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None, height=200)
        question_box.add_widget(options_box)

        # Thêm 2 đáp án mặc định
        for _ in range(2):
            self._add_option_field(options_box, question_box.radio_group)

        # Hàng nút “Thêm/Xóa đáp án”
        control_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        add_btn = Button(text="➕ Thêm đáp án", background_color=(1, 1, 1, 0.2), color=(1, 1, 1, 1))
        remove_btn = Button(text="🗑️ Xóa đáp án cuối", background_color=(1, 1, 1, 0.2), color=(1, 1, 1, 1))
        add_btn.bind(on_release=lambda *_: self._add_option_field(options_box, question_box.radio_group))
        remove_btn.bind(on_release=lambda *_: self._remove_option_field(options_box))
        control_box.add_widget(add_btn)
        control_box.add_widget(remove_btn)
        question_box.add_widget(control_box)

        container.add_widget(question_box)

    def _add_option_field(self, parent_box, radio_group):
        line = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        rb = ToggleButton(group=radio_group, size_hint_x=0.15, text="", allow_no_selection=False)
        txt = TextInput(
            hint_text=f"Đáp án {len(parent_box.children) + 1}",
            size_hint_x=0.85,
            background_color=(1, 1, 1, 0.25),
            foreground_color=(1, 1, 1, 1),
            font_size=16,
        )
        line.add_widget(rb)
        line.add_widget(txt)
        parent_box.add_widget(line)

    def _remove_option_field(self, parent_box):
        if parent_box.children:
            parent_box.remove_widget(parent_box.children[0])

    def save_quiz(self):
        quiz_name = self.ids.quiz_name.text.strip()
        if not quiz_name:
            self._popup("Lỗi", "Vui lòng nhập tên Quiz!")
            return

        container = self.ids.question_container
        if not container.children:
            self._popup("Lỗi", "Quiz cần ít nhất 1 câu hỏi!")
            return

        # Tạo quiz
        quiz_id = quiz_services.create_quiz(
            user_id="000000000000000000000000", title=quiz_name, description=""
        )

        # Duyệt từng câu hỏi
        for q_box in reversed(container.children):
            q_input = q_box.children[-3]  # TextInput đầu tiên
            q_text = q_input.text.strip()
            if not q_text:
                continue

            options_box = q_box.children[-2]
            options = []
            correct_answer = None

            for line in reversed(options_box.children):
                rb, txt = line.children
                val = txt.text.strip()
                if val:
                    if val in options:
                        self._popup("Lỗi", f"Đáp án bị trùng trong câu hỏi: {q_text}")
                        return
                    options.append(val)
                    if rb.state == "down":
                        correct_answer = val

            if not correct_answer:
                self._popup("Lỗi", f"Câu hỏi '{q_text}' chưa chọn đáp án đúng!")
                return

            quiz_services.add_question(quiz_id, q_text, correct_answer, [{"text": o, "display_order": i+1} for i, o in enumerate(options)])

        self._popup("Thành công", f"Quiz '{quiz_name}' đã được tạo với {len(container.children)} câu hỏi!")
        self.clear_inputs()

    def clear_inputs(self):
        self.ids.quiz_name.text = ""
        self.ids.question_container.clear_widgets()
        self.add_question_block()

    def _popup(self, title, msg):
        Popup(title=title, content=Label(text=msg, font_size=16), size_hint=(0.6, 0.35)).open()

    def go_back(self):
        self.manager.current = "teacher_home"
