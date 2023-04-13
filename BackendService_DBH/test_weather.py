import requests
import json

# Get the coordinate of Dublin city from Geocoding API
# reading the config file to get the token

with open("config.json", "r") as jsonfile:
    configFile = json.load(jsonfile)
    print("successfully loading Json config file...")
print("reading config file:", configFile)
token = configFile['weather_token']
url1 = f'http://api.openweathermap.org/geo/1.0/direct?q=Dublin&limit=1&appid={token}'
response_geo = requests.get(url1)

# check the response status
response_statusCode = response_geo.status_code
print(response_statusCode)  # return 200 means OK

# Get the coordinate and pass the variable
response_coordinate = response_geo.text
coordinate_Json = json.loads(response_coordinate)
print(coordinate_Json[0]['name'])
print(coordinate_Json[0]['lon'])
print(coordinate_Json[0]['lat'])
lon = coordinate_Json[0]['lon']
lat = coordinate_Json[0]['lat']

# invoke the weather API Using existing coordinate
url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}'  # Current weather data API
try:
    response_rawWeather = requests.get(url)
except Exception as e:
    print(e)

# check the response status
response_statusCode2 = response_rawWeather.status_code
print("weather API response code:", response_statusCode2)  # return 200 means OK

# Get the weather JSON data
response_weather = response_rawWeather.text
weather_data = json.loads(response_weather)  # Convert from JSON to Python

# Extract the fields of interest
id = weather_data['id']
weather_main = weather_data['weather'][0]['main']
temp = weather_data['main']['temp']
temp_feel = weather_data['main']['feels_like']
wind_speed = weather_data['wind']['speed']

# Create a dictionary to store the extracted data
data = {
    "id": id,
    "weather_main": weather_main,
    "temp": round((temp - 273.15), 1),  # convert temperature to celsius and keep one decimal place
    "temp_feel": round((temp_feel - 273.15)),
    "wind_speed": wind_speed
}

weather_result = json.dumps(data, indent=3)  # # Convert the dictionary to JSON
print(weather_result)
