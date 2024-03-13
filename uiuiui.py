from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('whatever.kv')

# Grid layout
class MyGridLayout(Widget):
    name = ObjectProperty(None)
    # pizza = ObjectProperty(None)
    # color = ObjectProperty(None)

    # def __init__(self, **kwargs):
    #     super(MyGridLayout, self).__init__(orientation='vertical',**kwargs)

    #     # Set columns
    #     self.cols = 0

    #     # Enter code box
    #     self.add_widget(Label(text="Enter code"))

    #     # Enter code input
    #     self.enter_code = TextInput(multiline = False)
    #     self.add_widget(self.enter_code)

    #     # Enter Continue as Guest Box
    #     self.continue_as_guest_button = Button(text="Continue as Guest")
    #     self.continue_as_guest_button.bind(on_press=self.press)
    #     self.add_widget(self.continue_as_guest_button)

    def press(self):
        print('continue as guess pressed')

class AwesomeApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    AwesomeApp().run()
