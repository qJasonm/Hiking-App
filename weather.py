import requests
import time

def temp_converter(kelvin_temp):
    return (kelvin_temp - 273.15)*(9/5)+32

city = 'denver'
api_key = '77ccac5efac3aa383ec4263be801fe61'
# geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={city},co,us&limit=1&appid={api_key}'
# geo_info = (requests.get(geo_url)).json()
# lat,lon = geo_info[0]['lat'],geo_info[0]['lon']

# weather_info_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
weather_info_url = f'https://api.openweathermap.org/data/2.5/weather?q={city},co,us&appid={api_key}'

weather_info = (requests.get(weather_info_url)).json()
weather_condition = (weather_info['weather'][0]['main'])
weather_temp = (round(temp_converter(weather_info['main']['temp'])))

print(f'Location: {city}\n'
      f'Weather: {weather_condition}\n'
      f'Temperature: {weather_temp}\n')
