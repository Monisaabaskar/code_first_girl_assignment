import requests

import emoji

from dotenv import load_dotenv
import os


from datetime import datetime, timedelta

load_dotenv()

## Step 1: Retrieve the API key from environment variables
API_KEY = os.getenv("API_key")

weather_emojis = {
    "thunderstorm with light rain": f"{emoji.emojize(':cloud with lightning:')}",
    "thunderstorm with rain":f"{emoji.emojize(':cloud with lightning:')}",
    "thunderstorm with heavy rain":f"{emoji.emojize(':cloud with lightning:')}",
    "light thunderstorm":f"{emoji.emojize(':cloud with lightning:')}",
    "thunderstorm":f"{emoji.emojize(':cloud with lightning:')}",
    "heavy thunderstorm":f"{emoji.emojize(':cloud with lightning:')}",
    "ragged thunderstorm":f"{emoji.emojize(':cloud with lightning:')}",
    "thunderstorm with light drizzle":f"{emoji.emojize(':cloud with lightning:')}",
    "thunderstorm with drizzle":f"{emoji.emojize(':cloud with lightning:')}",
    "thunderstorm with heavy drizzle":f"{emoji.emojize(':cloud with lightning:')}",
    "light intensity drizzle":f"{emoji.emojize(':sun behind rain cloud:')}",
    "drizzle":f"{emoji.emojize(':sun behind rain cloud:')}",
    "heavy intensity drizzle":f"{emoji.emojize(':sun behind rain cloud:')}",
    "light intensity drizzle rain":f"{emoji.emojize(':sun behind rain cloud:')}",
    "drizzle rain":f"{emoji.emojize(':sun behind rain cloud:')}",
    "heavy intensity drizzle rain":f"{emoji.emojize(':sun behind rain cloud:')}",
    "shower rain and drizzle":f"{emoji.emojize(':sun behind rain cloud:')}",
    "heavy shower rain and drizzle":f"{emoji.emojize(':sun behind rain cloud:')}",
    "shower drizzle":f"{emoji.emojize(':sun behind rain cloud:')}",
    "light rain":f"{emoji.emojize(':cloud with rain:')}",
    "moderate rain":f"{emoji.emojize(':cloud with rain:')}",
    "heavy intensity rain":f"{emoji.emojize(':cloud with rain:')}",
    "very heavy rain":f"{emoji.emojize(':cloud with rain:')}",
    "extreme rain":f"{emoji.emojize(':cloud with rain:')}",
    "freezing rain":f"{emoji.emojize(':cloud with rain:')}",
    "light intensity shower rain":f"{emoji.emojize(':cloud with rain:')}",
    "shower rain":f"{emoji.emojize(':cloud with rain:')}",
    "heavy intensity shower rain":f"{emoji.emojize(':cloud with rain:')}",
    "ragged shower rain":f"{emoji.emojize(':cloud with rain:')}",
    "light snow":f"{emoji.emojize(':snowflake:')}",
    "snow":f"{emoji.emojize(':snowflake:')}",
    "heavy snow":f"{emoji.emojize(':snowflake:')}",
    "sleet":f"{emoji.emojize(':snowflake:')}",
    "light shower sleet":f"{emoji.emojize(':snowflake:')}",
    "shower sleet":f"{emoji.emojize(':snowflake:')}",
    "light rain and snow":f"{emoji.emojize(':snowflake:')}",
    "rain and snow":f"{emoji.emojize(':snowflake:')}",
    "light shower snow":f"{emoji.emojize(':snowflake:')}",
    "shower snow":f"{emoji.emojize(':snowflake:')}",
    "heavy shower snow":f"{emoji.emojize(':snowflake:')}",
    "mist":f"{emoji.emojize(':fog:')}",
    "smoke":f"{emoji.emojize(':fog:')}",
    "haze":f"{emoji.emojize(':fog:')}",
    "sand/dust whirls":f"{emoji.emojize(':tornado:')}",
    "fog":f"{emoji.emojize(':fog:')}",
    "sand":f"{emoji.emojize(':fog:')}",
    "dust":f"{emoji.emojize(':fog:')}",
    "volcanic ash":f"{emoji.emojize(':fog:')}",
    "squalls":f"{emoji.emojize(':wind face:')}",
    "tornado":f"{emoji.emojize(':tornado:')}",
    "clear sky":f"{emoji.emojize(':sun:')}",
    "few clouds": f"{emoji.emojize(':sun_behind_large_cloud:')}",
    "scattered clouds":f"{emoji.emojize(':sun_behind_large_cloud:')}",
    "broken clouds":f"{emoji.emojize(':cloud:')}",
    "overcast clouds":f"{emoji.emojize(':fog:')}",
    "sunrise":f"{emoji.emojize(':sunrise:')}",
    "sunset":f"{emoji.emojize(':sunset:')}"
}

def API_by_city_name(city, country):
    
    ## Step 2: Define the base URL and the endpoint
    ## Step 3: Specify the parameters for the API request
    ## Step 4: Make the API request

    geocoding_api_response = \
        requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={API_KEY}")
    geocoding_city_coord = geocoding_api_response.json()
   
   

    lat = geocoding_city_coord[0]["lat"]
    lon = geocoding_city_coord[0]["lon"]

    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")
    
    ## Step 5: Parse the JSON response
    data = response.json()
    
    ## Step 6: Check the response status code and handle error
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

    lat = geocoding_zip_code_coord["lat"]
    lon = geocoding_zip_code_coord["lon"]

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
    for_description_emoji = weather_data["weather"][0]["description"]
    temperature_celsius = round(weather_data["main"]["temp"] - 273.15, 2)
    feel_like = round(weather_data["main"]["feels_like"] - 273.15, 2)
    max_temp = round(weather_data["main"]["temp_max"] -273.15)
    min_temp = round(weather_data["main"]["temp_min"] -273.15)
    pressure = weather_data["main"]["pressure"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    wind_direction = weather_data["wind"]["deg"]
    rain = weather_data.get("rain", {}).get('1h', 0)
    snow = weather_data.get("snow", {}).get('1h', 0) 
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

    weather_emoji = weather_emojis.get(for_description_emoji, "🌈")
    sunrise_emoji = weather_emojis.get("sunrise")
    sunset_emoji = weather_emojis.get("sunset")
    degree_symbol = u'\N{DEGREE SIGN}'

    output = f"""
    {weather_emoji}
    {datetime.now().strftime("%B %d, %I:%M%p")}
    {city}
    {temperature_celsius}{degree_symbol}C
    Sunrise{sunrise_emoji} | Sunset{sunset_emoji}
    {sunrise_local}{(len("Sunrise") - len(str(sunrise_local))+2) * " "} | {sunset_local}

    Feels like {feel_like}{degree_symbol}C. 
    {description} {weather_emoji}
    Max/Min temperature : {max_temp}{degree_symbol}C / {min_temp}{degree_symbol}C
    Humidity : {humidity} %
    Pressure : {pressure} hPa
    Wind : {wind_speed} m/s {wind_cardinal_direction}
    Visibility : {visibility} km
    Dew point: {dew_point} {degree_symbol}C
    Rain: {rain} mm
    snow: {snow} mm
    UV Index: {uvi_index}
    """

    output_without_emoji = f"""
    Today's Weather:

    {datetime.now().strftime("%B %d, %I:%M%p")}
    {city}
    {temperature_celsius} degree Celsius
    Sunrise | Sunset
    {sunrise_local}{(len("Sunrise") - len(str(sunrise_local))) * " "} | {sunset_local}

    Feels like {feel_like} degree Celsius. {description}
    Max/Min temperature : {max_temp} / {min_temp} degree Celsius
    Humidity : {humidity} %
    Pressure : {pressure} hPa
    Wind : {wind_speed} m/s {wind_cardinal_direction}
    Visibility : {visibility} km
    Dew point: {dew_point} degree Celsius
    Rain: {rain} mm
    snow: {snow} mm
    UV Index: {uvi_index}
    """

    return output, output_without_emoji


def UTC_to_local_time(utc_timestamp, offset_seconds):
    utc_time = datetime.utcfromtimestamp(utc_timestamp)
    offset = timedelta(seconds=offset_seconds)
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

formatted_weather, formatted_weather_without_emoji = weather_format(weather_data)
print(formatted_weather)

with open("weather_panda.txt", "w") as weather_forecast:
    weather_forecast.write(formatted_weather_without_emoji)
