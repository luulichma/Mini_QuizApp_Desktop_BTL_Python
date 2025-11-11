from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from threading import Thread
from app.services import chatbot_service

class ChatbotScreen(Screen):
    def on_enter(self):
        # make sure messages container is clear
        # Ensure messages container exists; if kv didn't register ids, create a fallback container
        mc = None
        try:
            mc = self.ids.get('messages_container')
        except Exception:
            mc = None

        if mc is None:
            # create a simple container as fallback
            mc = BoxLayout(orientation='vertical', size_hint_y=None)
            mc.height = 0
            self._messages_container = mc
            # add to root for visibility
            try:
                self.add_widget(mc)
            except Exception:
                pass
        else:
            mc.clear_widgets()

    def add_message(self, text: str, is_user: bool = False):
        # Defensive access to messages container (kv might not have registered ids)
        container = None
        try:
            container = self.ids.get('messages_container')
        except Exception:
            container = None

        if container is None:
            container = getattr(self, '_messages_container', None)

        if container is None:
            # As a last resort, print to console and do nothing UI-wise
            print(f"Chatbot: cannot find messages container to display: {text}")
            return

        # Ensure text color contrasts with typical light background
        text_color = (0.08, 0.08, 0.08, 1)
        if is_user:
            lbl = Label(text=f"[b]Bạn:[/b] {text}", markup=True, size_hint_y=None, color=text_color)
        else:
            lbl = Label(text=f"[b]Bot:[/b] {text}", markup=True, size_hint_y=None, color=text_color)
        lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1] + 20))
        container.add_widget(lbl)

        # scroll to bottom if possible
        try:
            if hasattr(self.ids, 'messages_scroll') and self.ids.get('messages_scroll'):
                Clock.schedule_once(lambda dt: self.ids.messages_scroll.scroll_to(lbl), 0.05)
        except Exception:
            pass

    def send_message(self):
        text = self.ids.chat_input.text.strip()
        if not text:
            return
        # Debug: log send attempt
        try:
            print(f"Chatbot: send_message called with: {text}")
        except Exception:
            pass

        # show user message
        self.add_message(text, is_user=True)
        self.ids.chat_input.text = ''

        # call service in background
        def worker(prompt):
            try:
                print(f"Chatbot: worker started for prompt: {prompt}")
            except Exception:
                pass
            try:
                resp = chatbot_service.ask(prompt)
                try:
                    print(f"Chatbot: worker received response: {resp}")
                except Exception:
                    pass
            except Exception as e:
                resp = f"Lỗi: {str(e)}"

            # add to UI thread via Clock.schedule_once
            def update_ui(dt):
                self.add_message(resp, is_user=False)

            Clock.schedule_once(update_ui, 0)

        # start background thread
        thread = Thread(target=worker, args=(text,), daemon=True)
        thread.start()

    def go_back(self):
        """Navigate back to home screen based on current user role"""
        try:
            app = App.get_running_app()
            # Prefer explicit app.current_user_role if set
            role = None
            if hasattr(app, 'current_user_role') and app.current_user_role:
                role = app.current_user_role
            # Fall back to app.user dict set by login
            elif hasattr(app, 'user') and isinstance(app.user, dict):
                role = app.user.get('role')

            if role == 'teacher':
                self.manager.current = 'teacher_home'
            else:
                # default and student both go to student_home
                self.manager.current = 'student_home'
        except Exception:
            self.manager.current = 'student_home'
