from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import *
from tkhtmlview import HTMLLabel
from utils import get_settings
from api import WeatherData, get_raw_data


env = get_settings()
root = Tk()
root.title("Weather App")
root.iconbitmap("weather.ico")
root.geometry("670x400")


# Top frame
top_frame = LabelFrame(root, text="Location", padding=5)
top_frame.grid(row=0, column=0)


def refresh():
    txt = location_input.get()
    show_weather_data(txt)


# Widgets
refresh_btn = Button(top_frame,
                     text="Refresh",
                     command=refresh,
                     compound=TOP)
refresh_btn.grid(row=0, column=1)
location_input = Entry(top_frame, width=30)
location_input.insert(0, env.get("LOCATION"))
location_input.grid(row=0, column=0)

# Frame seperator
seperator = Separator(root, orient='horizontal')
seperator.place(relx=0, rely=0.75)

# Weather frame
weather_frame = LabelFrame(root, text="Weather", padding=4)
weather_frame.grid(row=1, column=0)


def show_weather_data(q: str):
    data = get_raw_data(q, env.get("API_KEY"), env.get("UNIT"))
    if isinstance(data, str):
        showerror("Error", message=data)
        return
    weather_data = WeatherData.parse_data(data, env.get("UNIT"))

    # Widgets
    weather = HTMLLabel(weather_frame, html=f"""
    <p>
        <strong>{weather_data.weather}</strong>{'&nbsp;' * 3}<img src="{weather_data.icon}">
        <br>
        <i>{weather_data.description}</i>
    </p>
    <br><br>    
    <p>
        <b>Temperature: </b>{weather_data.temp}{'&nbsp;' * 4}<b>Min/Max: </b>{weather_data.temp_min} / {weather_data.temp_max}
    </p>
    <br>
    <p>
        <b>Pressure: </b>{weather_data.pressure}{'&nbsp;' * 9}<b>Humidity: </b>{weather_data.humidity}
    </p> 
    <br>
    <p>
        <b>Visibility: </b>{weather_data.visibility}{'&nbsp;' * 14}<b>Wind: </b>{weather_data.wind_speed} {weather_data.wind_direction}
    </p>
    <br>
    <p>
        <b>Cloudiness: </b>{weather_data.cloudiness}
    </p>
    """)
    weather.fit_height()
    weather.grid(row=0, column=0)


show_weather_data(env.get("LOCATION"))


if __name__ == "__main__":
    root.grid_columnconfigure(1, pad=0, weight=1)
    root.mainloop()
