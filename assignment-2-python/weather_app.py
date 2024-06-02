import requests

import emoji

from dotenv import load_dotenv
import os

import json

from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv("API_key")

def API_by_city_name(city, country):
    geocoding_api_response = \
        requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={API_KEY}")
    geocoding_city_coord = geocoding_api_response.json()
   

    lat = geocoding_city_coord[0]["lat"]
    lon = geocoding_city_coord[0]["lon"]

    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")
    data = response.json()
    #print(data)
    if data and response.status_code == 200:
        return data
    
    elif data and response.status_code == 500:
        print("Server error response")

    else:
        print("Client error response")
    


def API_by_zipcode(zip_code, country):
    geocoding_api_response = \
        requests.get(f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country}&appid={API_KEY}")
    geocoding_zip_code_coord = geocoding_api_response.json()

    lat = geocoding_zip_code_coord[0]["lat"]
    lon = geocoding_zip_code_coord[0]["lon"]

    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")
    data = response.json()
    if (data and response.status_code) == 200:
        return(data)
    
    elif data and response.status_code == 500:
        print("Server error response")

    else:
        print("Client error response")


def weather_format(weather_data):
    weather = weather_data["weather"][0]["main"]
    description = weather_data["weather"][0]["description"].capitalize()
    temperature_celsius = round(weather_data["main"]["temp"] - 273.15, 2)
    feel_like = round(weather_data["main"]["feels_like"] - 273.15, 2)
    max_temp = round(weather_data["main"]["temp_max"] -273.15)
    min_temp = round(weather_data["main"]["temp_min"] -273.15)
    pressure = weather_data["main"]["pressure"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    wind_direction = weather_data["wind"]["deg"]
    rain = weather_data.get("rain", {}).get('1h', 0) 
    dew_point = weather_data["main"].get("dew_point", "N/A")
    uvi_index = weather_data.get("uvi", "N/A")
    visibility = weather_data["visibility"] / 1000
    sunrise = weather_data["sys"]["sunrise"]
    sunset = weather_data["sys"]["sunset"]
    city = weather_data["name"]
    date_time = weather_data["dt"]
    timezone = weather_data["timezone"]
    wind_cardinal_direction = convert_wind_direction(wind_direction)
    sunrise_local = UTC_to_local_time(sunrise, timezone).strftime('%H:%M')
    sunset_local = UTC_to_local_time(sunset, timezone).strftime('%H:%M')


    output = f"""
    {datetime.now().strftime("%B %d, %I:%M%p")}
    {city}
    {temperature_celsius}{chr(176)}C
    Sunrise | Sunset
    {sunrise_local}{(len("Sunrise") - len(str(sunrise_local))) * " "} | {sunset_local}

    Feels like {feel_like}{chr(176)}C. {description}.
    Max/Min temperature : {max_temp}{chr(176)}C / {min_temp}{chr(176)}C
    Humidity : {humidity} %
    Pressure : {pressure} hPa
    Wind : {wind_speed} m/s {wind_cardinal_direction}
    Visibility : {visibility} km
    Dew point: {dew_point} {chr(176)}C
    Rain: {rain} mm
    UV Index: {uvi_index}
    """
    return output

def UTC_to_local_time(utc_timestamp, offset_seconds):
    # Convert the UTC timestamp to a datetime object
    utc_time = datetime.utcfromtimestamp(utc_timestamp)

    # Create a timedelta object for the offset
    offset = timedelta(seconds=offset_seconds)

    # Calculate the local time by adding the offset to the UTC time
    local_time = utc_time + offset

    return(local_time)

def convert_wind_direction(wind_direction):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(wind_direction / 22.5) % 16
    return directions[index]




user_input = input("Enter the '1' to search by city name or '2' to search by zipcode? ")

if user_input == '1':
    city_name = input("Enter the City name ? ")
    city = city_name.lower()
    country_name = input ("Enter the Country name (e.g., 'us' for united states)? ")
    country = country_name.lower()
    weather_data = API_by_city_name(city, country)

elif user_input == "2":
    zip_code = input("Enter the zip code ? ")
    country_name = input ("Enter the Country name (e.g., 'us' for united states)? ")
    country = country_name.lower()
    weather_data = API_by_zipcode(zip_code, country)

else:
    print("Invaild Input")

formatted_weather = weather_format(weather_data)
print(formatted_weather)

with open("weather_panda.txt", "w") as weather_forecast:
    weather_forecast.write(formatted_weather)
