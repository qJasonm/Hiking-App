from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import mainthread
from kivy.config import Config
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy_garden.mapview import MapView
import socket
import threading
import requests
from kivy.config import Config
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
Config.set('graphics', 'fullscreen', 1)
# Window.size = (350,600)
HOST = '35.197.2.183'
PORT = 3030
Builder.load_file('my.kv')

map_dict = {'1111':"lair o'the bear",'2222':'cherry creek','3333':"sloan's lake"}

class SigninPage(Screen):
    def go_to_knowledge(self, trail_code):
        self.manager.current = 'knowledge'
        self.manager.get_screen('knowledge').update_data(trail_code)

    def go_to_general(self):
        self.manager.current = 'general'
        self.manager.get_screen('general')

class GuestScreen(Screen):
    def print_passcode(self, passcode):
        print(f'Entered passcode is: {passcode}')

class Weather:
    def get_weather(self, trail_name: str):
        if trail_name.lower() == "1111":
            weather_info_url = "https://bear.qjasonma.com/Lairo'thebear/json"
        elif trail_name.lower() == '2222':
            weather_info_url = "https://bear.qjasonma.com/CherryCreek/json"
        elif trail_name.lower() == '3333':
            weather_info_url = "https://bear.qjasonma.com/Sloanslake/json"
        weather_info = (requests.get(weather_info_url)).json()

        weather_condition = weather_info['weather']
        weather_temp = weather_info['temperature']
        weather_visibility = weather_info['visibility']
        weather_windspeed = weather_info['wind_speed']
        city = weather_info['city']
        prediction = weather_info['prediction']['advice']
        
        return (weather_condition, weather_temp, weather_visibility, weather_windspeed, city, prediction)

class KnowledgeScreen(Screen):
    map_lat = ObjectProperty('39.7392')  
    map_lon = ObjectProperty('-104.9903')  
    map_zoom = ObjectProperty('10')  
    show_map = BooleanProperty(False)
    def update_data(self, trail_code_input):
        self.ids.location.text = str(map_dict[trail_code_input]).upper()
        weather = Weather()
        weather_condition, weather_temp, weather_visibility, weather_windspeed, city, prediction = weather.get_weather(trail_code_input)
        # Update weather labels with fetched information
        self.ids.weather_condition.text = f"{weather_condition}"
        self.ids.temperature.text = f"{weather_temp}°F"
        self.ids.visibility.text = f"{weather_visibility}"
        self.ids.wind.text = f"{weather_windspeed} m/s"
        self.ids.city.text = city
        self.ids.prediction.text = prediction

        if weather_condition == 'Clear':
            self.ids.sum_image.source = 'sunny.png'
        elif weather_condition == 'Rain':
            self.ids.sum_image.source = 'rainy.png'
        elif weather_condition == 'Clouds':
            self.ids.sum_image.source = 'clouds.png'
        elif weather_condition == 'Snow':
            self.ids.sum_image.source = 'snow.png'

        if trail_code_input.lower() == "lairo'thebear":
            self.ids.mapview.lat = '39.66825309799876'  
            self.ids.mapview.lon = '-105.25672674719111'
        elif trail_code_input.lower() == 'cherry creek':
            self.ids.mapview.lat = '39.69145184179065' 
            self.ids.mapview.lon = '-104.9144065293836' 
        elif trail_code_input.lower() == 'sloan lake':
            self.ids.mapview.lat = '39.74487181981862'  
            self.ids.mapview.lon = '-105.0447771796079' 
    def connect(self):
        self.manager.current = 'connect_screen'

    def exit(self):
        self.manager.current = 'sign_in'
    def toggle_map(self):
        self.show_map = not self.show_map
class GeneralScreen(Screen):
    def exit(self):
        self.manager.current = 'sign_in'
    pass

class ConnectScreen(Screen):
    username_input = ObjectProperty(None)

    def connect(self):
        self.manager.current = 'chat_screen'
        username = self.username_input.text
        self.manager.get_screen('chat_screen').connect(username)
    def exit(self):
        self.manager.current = 'sign_in'

class ChatScreen(Screen):
    chat_log = ObjectProperty(None)
    chat_input = ObjectProperty(None)

    def connect(self, username=''):
        self.username = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.client.sendall(username.encode())  # send username to server
        threading.Thread(target=self.listen_for_messages_from_server, daemon=True).start()

    def exit(self):
        self.manager.current = 'sign_in'

    def listen_for_messages_from_server(self):
        while True:
            message = self.client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]
                message = f"[{username}] {content}"
            else:
                message = "Message received from client is empty"
            self.update_chat_log(message)
            
    
    def disconnect(self):
        if self.client:
            self.client.close()
            self.manager.current = 'connect_screen'
            self.chat_log.text = ''

    @mainthread
    def update_chat_log(self, message):
        self.chat_log.text += message + '\n'

    def send_message(self):
        message = self.chat_input.text
        if message != '':
            self.client.sendall(message.encode())
        else:
            self.chat_log.text += "Message cannot be empty\n"
        
class ScreenManagement(ScreenManager):
    pass

class TrailApp(App):
    def build(self):
        self.icon = 'bear.jpg'
        return ScreenManagement()

if __name__ == '__main__':
    TrailApp().run()
