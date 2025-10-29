from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from app.services import quiz_services
from app.services.quiz_services import get_quiz_details, update_quiz


class QuizCreateScreen(Screen):
    editing_quiz_id = None

    def load_quiz_for_editing(self, quiz_id):
        """Tải dữ liệu của một quiz và hiển thị trên màn hình để sửa."""
        self.editing_quiz_id = quiz_id
        quiz_data = get_quiz_details(quiz_id)

        if not quiz_data:
            self._popup("Lỗi", "Không thể tải dữ liệu quiz.")
            self.cancel_editing()
            return

        # Thay đổi giao diện sang chế độ sửa
        self.ids.screen_title.text = "Sửa Quiz"
        self.ids.quiz_name.text = quiz_data.get('title', '')
        self.ids.quiz_description.text = quiz_data.get('description', '')
        self.children[0].children[0].children[0].text = "Cập nhật Quiz" # Tìm nút "Tạo Quiz" và đổi tên

        # Xóa các câu hỏi mặc định và tải câu hỏi của quiz
        container = self.ids.question_container
        container.clear_widgets()

        for question in quiz_data.get('questions', []):
            self.add_question_block_with_data(question)

    def add_question_block_with_data(self, question_data):
        """Tạo một khối câu hỏi và điền dữ liệu có sẵn."""
        container = self.ids.question_container
        # Code tương tự add_question_block nhưng điền sẵn dữ liệu
        question_box = BoxLayout(orientation="vertical", size_hint_y=None, height=300, spacing=10)
        question_box.question_index = len(container.children) + 1
        question_box.radio_group = f"group_{question_box.question_index}"

        q_input = TextInput(
            text=question_data.get('question_title', ''),
            size_hint_y=None, height=60, background_color=(1, 1, 1, 0.25),
            foreground_color=(1, 1, 1, 1), font_size=16, padding=[10, 8],
        )
        question_box.add_widget(q_input)

        options_box = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None, height=200)
        question_box.add_widget(options_box)

        # Thêm các đáp án đã có
        for option in question_data.get('options', []):
            self._add_option_field_with_data(options_box, question_box.radio_group, option, question_data.get('correct_answer'))

        control_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        add_btn = Button(text="➕ Thêm đáp án", background_color=(1, 1, 1, 0.2), color=(1, 1, 1, 1))
        remove_btn = Button(text="🗑️ Xóa đáp án cuối", background_color=(1, 1, 1, 0.2), color=(1, 1, 1, 1))
        add_btn.bind(on_release=lambda *_: self._add_option_field(options_box, question_box.radio_group))
        remove_btn.bind(on_release=lambda *_: self._remove_option_field(options_box))
        control_box.add_widget(add_btn)
        control_box.add_widget(remove_btn)
        question_box.add_widget(control_box)

        container.add_widget(question_box)

    def _add_option_field_with_data(self, parent_box, radio_group, option_data, correct_answer):
        """Thêm một dòng đáp án và điền dữ liệu có sẵn."""
        line = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        rb = ToggleButton(group=radio_group, size_hint_x=0.15, text="", allow_no_selection=False)
        if option_data['text'] == correct_answer:
            rb.state = 'down'
        
        txt = TextInput(
            text=option_data['text'],
            size_hint_x=0.85, background_color=(1, 1, 1, 0.25),
            foreground_color=(1, 1, 1, 1), font_size=16,
        )
        line.add_widget(rb)
        line.add_widget(txt)
        parent_box.add_widget(line)

    def cancel_editing(self):
        """Reset màn hình về trạng thái tạo mới."""
        self.editing_quiz_id = None
        self.ids.screen_title.text = "Create Quiz"
        self.clear_inputs()
        self.children[0].children[0].children[0].text = "Tạo Quiz"

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
        quiz_description = self.ids.quiz_description.text.strip()
        if not quiz_name:
            self._popup("Lỗi", "Vui lòng nhập tên Quiz!")
            return

        container = self.ids.question_container
        if not container.children:
            self._popup("Lỗi", "Quiz cần ít nhất 1 câu hỏi!")
            return

        # Thu thập dữ liệu từ UI
        questions_data = []
        for q_box in reversed(container.children):
            q_input = q_box.children[-1] # Sửa index từ -3 thành -1
            q_text = q_input.text.strip()
            if not q_text:
                continue

            options_box = q_box.children[-2]
            options = []
            correct_answer = None

            for line in reversed(options_box.children):
                txt, rb = line.children
                val = txt.text.strip()
                if val:
                    if val in [opt['text'] for opt in options]:
                        self._popup("Lỗi", f"Đáp án bị trùng trong câu hỏi: {q_text}")
                        return
                    options.append({"text": val, "display_order": len(options) + 1})
                    if rb.state == "down":
                        correct_answer = val
            
            if not correct_answer:
                self._popup("Lỗi", f"Câu hỏi '{q_text}' chưa chọn đáp án đúng!")
                return
            
            questions_data.append({
                'question_title': q_text,
                'correct_answer': correct_answer,
                'options': options
            })

        if not questions_data:
            self._popup("Lỗi", "Không có câu hỏi hợp lệ nào.")
            return

        # Kiểm tra nếu đang sửa hay tạo mới
        if self.editing_quiz_id:
            # Chế độ sửa
            update_quiz(self.editing_quiz_id, quiz_name, quiz_description, questions_data)
            self._popup("Thành công", f"Quiz '{quiz_name}' đã được cập nhật!", self.go_to_library)
        else:
            # Chế độ tạo mới
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
                quiz_services.add_question(quiz_id, q_data['question_title'], q_data['correct_answer'], q_data['options'])

            self._popup("Thành công", f"Quiz '{quiz_name}' đã được tạo!", self.go_to_library)

    def go_to_library(self, *args):
        """Callback function to clear inputs and navigate to the library."""
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
