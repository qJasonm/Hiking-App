from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
Window.size = (350,600)




class WeatherApp(MDApp):
    def build(self):
        return Builder.load_file('weather.kv')

if __name__ == '__main__':
    WeatherApp().run()

