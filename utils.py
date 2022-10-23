from datetime import datetime
import humanize
import json


def get_time(t: int) -> str:
    d = datetime.fromtimestamp(t).replace(tzinfo=None).astimezone(tz=None)
    return humanize.naturaltime(d)


def deg_to_compass(deg) -> str:
    val = int((deg / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


def get_units() -> dict:
    with open("units.json", 'r') as file:
        data = json.load(file)
    return data


def get_settings() -> dict:
    with open("settings.json", 'r') as file:
        data = json.load(file)
    return data
