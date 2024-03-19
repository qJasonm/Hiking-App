from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('my.kv')

# Grid layout
class SigninPage(Screen):
    pass

class GuestScreen(Screen):
    def print_passcode(self):
        print(f'Entered passcode is: {self.ids.passcode.text}')


class ScreenManagement(ScreenManager):
    pass

class TrailApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == '__main__':
    TrailApp().run()
