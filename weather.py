import requests
import time

class Weather:
    def temp_converter(self, kelvin_temp):
        return (kelvin_temp - 273.15)*(9/5)+32
    
    def get_weather(self, trail_name: str):
        api_key = '77ccac5efac3aa383ec4263be801fe61'
        weather_info_url = "https://bear.qjasonma.com/Lairo'thebear/json"

        weather_info = (requests.get(weather_info_url)).json()

        weather_condition = weather_info['weather']
        weather_temp = weather_info['temperature']
        weather_visibility = weather_info['visibility']
        weather_windspeed = weather_info['wind_speed']
        city = weather_info['city']
        prediction = weather_info['prediction']['advice']
        
        return (city, weather_condition, weather_temp, weather_visibility, weather_windspeed, city, prediction)
        
weather = Weather()
weather.get_weather("denver")