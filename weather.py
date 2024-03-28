import requests
import time

class Weather:
    def temp_converter(self, kelvin_temp):
        return (kelvin_temp - 273.15)*(9/5)+32
    
    def get_weather(self, city: str):
        api_key = '77ccac5efac3aa383ec4263be801fe61'
        weather_info_url = f'https://api.openweathermap.org/data/2.5/weather?q={city},co,us&appid={api_key}'

        weather_info = (requests.get(weather_info_url)).json()
        weather_condition = (weather_info['weather'][0]['main'])
        weather_temp = (round(self.temp_converter(weather_info['main']['temp'])))

        print(f'Location: {city}\n'
            f'Weather: {weather_condition}\n'
            f'Temperature: {weather_temp}\n')
        
        return (weather_condition, weather_temp)
        
