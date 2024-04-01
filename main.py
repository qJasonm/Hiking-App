from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from weather import Weather
from kivy.clock import mainthread
from kivy.config import Config
import socket
import threading

HOST = '127.0.0.1'
PORT = 8080
Builder.load_file('my.kv')

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

class KnowledgeScreen(Screen):
    def __init__(self, **kwargs):
        super(KnowledgeScreen, self).__init__(**kwargs)
        self.trail_code = '' 

    def update_data(self, trail_code_input):
        self.ids.trail_code_display.text = 'Trail Code: ' + trail_code_input
        weather = Weather()
        if trail_code_input == '123':
            weather_condition, weather_temp = weather.get_weather("denver")
            self.ids.weather.text = str(weather_temp) + "  oF" + "\n" + weather_condition
            self.ids.alert.text = "Alert: " + "Strong winds"
            self.ids.more_info.text = "More Info: " + "Nice trail ahead !"
            self.ids.warning.text = "Warning: " + "Beware of Bears"
            self.ids.map_image.source = "cherry-creek.png"

    def connect(self):
        self.manager.current = 'connect_screen'
        # self.manager.get_screen('connect_screen').connect

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


class ChatScreen(Screen):
    chat_log = ObjectProperty(None)
    chat_input = ObjectProperty(None)

    def connect(self, username=''):
        self.username = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.client.sendall(username.encode())  # send username to server
        threading.Thread(target=self.listen_for_messages_from_server, daemon=True).start()

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





# class MapWidget(Screen):
#     def __init__(self, **kwargs):
#         super(MapWidget, self).__init__(**kwargs)
#         self.size_hint = (1, 1)
#         self.bind(size=self.update)
        
#         # Example map data
#         self.add_widget(Label(text="Map Data: Latitude = 40.7128, Longitude = -74.0060", color=(0, 0, 0, 1)))

#         with self.canvas:
#             Color(1, 1, 1, 1)  # White background
#             self.rect = Rectangle(pos=self.pos, size=self.size)
    
#     def update(self, *args):
#         self.rect.pos = self.pos
#         self.rect.size = self.size
