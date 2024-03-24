from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

# Load the kv file
Builder.load_file('second_screen.kv')


class MapWidget(Widget):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.size_hint = (1, 1)
        self.bind(size=self.update)
        
        # Example map data
        self.add_widget(Label(text="Map Data: Latitude = 40.7128, Longitude = -74.0060", color=(0, 0, 0, 1)))

        with self.canvas:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(pos=self.pos, size=self.size)
    
    def update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MyBoxLayout(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == '__main__':
    MyApp().run()
