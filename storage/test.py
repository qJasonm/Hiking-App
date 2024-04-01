from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import socket
import threading
from kivy.properties import ObjectProperty
from kivy.clock import mainthread

HOST = '127.0.0.1'
PORT = 1234


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
            print(self.chat_log)
    
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
            

class MyApp(App):
    def build(self):
        return Builder.load_file('chat.kv')


if __name__ == '__main__':
    MyApp().run()
