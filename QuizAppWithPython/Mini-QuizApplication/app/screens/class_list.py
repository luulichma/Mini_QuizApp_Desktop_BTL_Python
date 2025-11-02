from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from app.services import class_services

class ClassListScreen(Screen):

    def on_enter(self, *args):
        self.load_classes()

    def load_classes(self):
        app = App.get_running_app()
        teacher_id = app.user.get('_id')

        if not teacher_id:
            self.go_back()
            return

        classes = class_services.list_classes_by_teacher(teacher_id)
        class_container = self.ids.class_container
        class_container.clear_widgets()

        if not classes:
            class_container.add_widget(Label(text="Chưa có lớp học nào.", size_hint_y=None, height=50))
            return

        for cls in classes:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=10, spacing=10)
            box.add_widget(Label(text=cls['class_name'], size_hint_x=0.7))
            
            details_button = Button(text="Chi tiết", size_hint_x=0.3)
            details_button.bind(on_release=lambda btn, class_id=cls['_id']: self.go_to_class_details(class_id))
            box.add_widget(details_button)
            
            class_container.add_widget(box)

    def go_to_class_details(self, class_id):
        class_details_screen = self.manager.get_screen('class_details')
        class_details_screen.class_id = class_id
        self.manager.current = 'class_details'

    def go_back(self, *args):
        self.manager.current = 'teacher_home'
