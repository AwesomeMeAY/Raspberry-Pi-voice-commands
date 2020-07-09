#!/usr/bin/python3
import subprocess
# Takes in a string gets rid of non int parts and converts string to int.
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
    # get weather data from wttr.in
    subprocess.call('curl wttr.in/Racine?format="%C:%t+%h+%l" > weather.txt', shell=True)
    forcast = open('weather.txt').read()

    # Slice the string to get separate weather items
    weather_condition = forcast[:forcast.index(":")]
    temperature = forcast[forcast.index("+"):forcast.index("F")]
    precipitation = intafy(forcast[forcast.index("F"):forcast.index("%")])
    city = forcast[forcast.index("%"):][2:]
    
    return f"It is {weather_condition} with a {precipitation} percent chance of precipitation at {intafy(temperature)} degrees Fahrenheit in {city}"

if __name__ == "__main__":
    print(forecast())
