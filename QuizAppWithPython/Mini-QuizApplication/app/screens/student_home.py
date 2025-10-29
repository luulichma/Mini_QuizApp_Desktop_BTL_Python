from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.factory import Factory
from app.services.quiz_services import get_results_by_user


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
        quiz_id = self.ids.quiz_id_input.text.strip()
        if not quiz_id:
            self._show_popup("Lỗi", "Vui lòng nhập ID bài quiz.")
            return

        # Lấy màn hình quiz player và gán ID
        quiz_player_screen = self.manager.get_screen('quiz_player')
        quiz_player_screen.quiz_id = quiz_id

        # Chuyển màn hình
        self.manager.current = 'quiz_player'

    def load_history(self):
        """Tải và hiển thị lịch sử các bài đã làm."""
        history_list_layout = self.ids.history_list
        history_list_layout.clear_widgets()

        if not self.current_user:
            history_list_layout.add_widget(Label(text="Vui lòng đăng nhập lại", color=(1, 1, 1, 0.9), font_size=18))
            return

        try:
            user_id = self.current_user.get("_id")
            results = get_results_by_user(user_id)

            if not results:
                history_list_layout.add_widget(Label(text="(Chưa có lịch sử làm bài)", color=(1, 1, 1, 0.9), font_size=18))
                return

            for result in results:
                item = Factory.HistoryListItem()
                item.ids.history_quiz_title.text = result['quiz_title']
                item.ids.history_quiz_score.text = f"Điểm: {result['score']}"
                history_list_layout.add_widget(item)
        except Exception as e:
            history_list_layout.add_widget(Label(text=f"Lỗi tải lịch sử: {e}", color=(1, 0.5, 0.5, 1)))

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