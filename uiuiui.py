from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('whatever.kv')

# Grid layout
class MyGridLayout(Widget):
    name = ObjectProperty(None)

    def press(self):
        print('continue as guess pressed')

class AwesomeApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    AwesomeApp().run()
