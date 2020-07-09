#!/usr/bin/python3
import subprocess
def intafy(string):
    int_only = ""
    for char in string:
        try:
            int(char)
            int_only += char
        except ValueError:
            continue
    return int(int_only)
def forecast():
    subprocess.call('curl wttr.in/Racine?format="%C:%t+%h+%l" > weather.txt', shell=True)
    forcast = open('weather.txt').read()
    print(forcast)
    weather_condition = forcast[:forcast.index(":")]
    temperature = forcast[forcast.index("+"):forcast.index("F")]
    percipitaion = intafy(forcast[forcast.index("F"):forcast.index("%")])
    city = forcast[forcast.index("%"):][2:]
    return(f"It is {weather_condition} with a {percipitaion} percent chance of percipitaion at {intafy(temperature)} degrees Fahrenheit in {city}")
if __name__ == "__main__":
    print(forecast())
