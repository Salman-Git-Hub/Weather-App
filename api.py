from typing import Union
import requests
from utils import *


class WeatherData:
    def __init__(self, weather, description, icon,
                 temp, temp_min, temp_max, pressure, humidity,
                 visibility, wind_speed, wind_direction, cloudiness, time):
        self.weather = weather
        self.description = description
        self.icon = icon
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.humidity = humidity
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.cloudiness = cloudiness
        self.time = time
        return

    @classmethod
    def parse_data(cls, data: dict, unit: str):
        weather_data = {}
        units = get_units()
        w = data.get("weather")[0]
        weather_data['weather'] = w.get("main")
        weather_data['description'] = w.get("description")
        weather_data['icon'] = f"https://openweathermap.org/img/w/{w.get('icon')}.png"
        m = data.get("main")
        weather_data['temp'] = f'{m.get("temp")} {units.get("temp").get(unit)}'
        weather_data['temp_min'] = f'{m.get("temp_min")} {units.get("temp").get(unit)}'
        weather_data['temp_max'] = f'{m.get("temp_max")} {units.get("temp").get(unit)}'
        weather_data['pressure'] = f'{m.get("pressure")} {units.get("pressure")}'
        weather_data['humidity'] = f'{m.get("humidity")} {units.get("humidity")}'
        weather_data['visibility'] = f'{data.get("visibility") / 1000} {units.get("visibility")}'
        wi = data.get("wind")
        weather_data['wind_speed'] = f'{wi.get("speed")} {units.get("wind_speed").get(unit)}'
        weather_data['wind_direction'] = deg_to_compass(wi.get("deg"))
        weather_data['cloudiness'] = f'{data.get("clouds").get("all")} {units.get("cloudiness")}'
        weather_data['time'] = get_time(data.get("dt"))
        return cls(**weather_data)


def get_raw_data(location, api_key, units) -> Union[str, dict]:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units}"
    r = requests.get(url)
    if r.status_code == 401:
        return "Invalid API Key"
    elif r.status_code == 404:
        return "Wrong city name"
    elif r.status_code == 429:
        return "Rate limit exceeded"
    else:  # status_code = 200
        data = r.json()
        return data
