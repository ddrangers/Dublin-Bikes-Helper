import json
import requests
import pickle
import os
import datetime

pickle_dir = "/Users/jingao/Documents/GitHub/Dublin-Bikes-Helper/BackendService_DBH/Pickle Files"
pickle_files = os.listdir(pickle_dir)
with open("config.json", "r") as jsonfile:
    configFile = json.load(jsonfile)
token = configFile['weather_token']
url1 = f'http://api.openweathermap.org/geo/1.0/direct?q=Dublin&limit=1&appid={token}'
response_geo = requests.get(url1)
# Get the coordinate and pass the variable
response_coordinate = response_geo.text
coordinate_Json = json.loads(response_coordinate)
lon = coordinate_Json[0]['lon']
lat = coordinate_Json[0]['lat']
# invoke the weather API Using existing coordinate
url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={token}'  # Forecast weather data API
try:
    response_rawWeather = requests.get(url)
except Exception as e:
    print(e)
# Get the weather JSON data
response_weather = response_rawWeather.text
weather_data = json.loads(response_weather)  # Convert from JSON to Python


def process_weather_data(weather_data):
    weather_map = {
        "Clouds": 2,
        "Rain": 4,
        "Snow": 5,
        "Clear": 1,
        "Drizzle": 3,
        "Mist": 6,
        "Fog": 7
    }

    weather_list = []
    for data in weather_data['list'][:8]:
        dt = datetime.datetime.fromtimestamp(data['dt'])
        web_month = dt.month
        web_day_of_week = dt.weekday()
        web_hour = dt.hour

        for _ in range(3):
            web_weather_main = weather_map.get(data['weather'][0]['main'], 0)
            web_clouds = data['clouds']['all']
            web_tempcel = data['main']['temp'] - 273.15
            web_weather_id = data['weather'][0]['id']
            web_wind_speed = data['wind']['speed']
            web_tempcel_feel = data['main']['feels_like'] - 273.15

            X_web = [web_weather_main, web_clouds, web_tempcel, web_weather_id, web_wind_speed, web_tempcel_feel,
                     web_month,
                     web_day_of_week, web_hour]

            weather_list.append(X_web)

            web_hour += 1  # Increment the hour
            if web_hour >= 24:
                web_hour = 0
                web_day_of_week += 1
                if web_day_of_week >= 7:
                    web_day_of_week = 0

    return weather_list[:24]


weather_list = process_weather_data(weather_data)
print(weather_list)
length_of_weather_list = len(weather_list)
print("Length of weather_list:", length_of_weather_list)


def get_station_number(file_name):
    return int(file_name.split("_")[0].replace("randomforest", ""))


def get_model_type(file_name):
    if file_name.endswith("_bike.pkl"):
        return "bike"
    elif file_name.endswith("_park.pkl"):
        return "park"
    else:
        return None


def load_model(model_type, station_number):
    for file_name in pickle_files:
        if station_number == get_station_number(file_name) and model_type == get_model_type(file_name):
            file_path = os.path.join(pickle_dir, file_name)
            with open(file_path, "rb") as f:
                model = pickle.load(f)
            return model
    return None


#======test cormac jupyter data===================================
# input_month = 3
# input_day_of_week = 1 #0 = Mon, 1 = Tues, 2 = Wed etc
# input_hour = 20
# input_weather_main = 4
# input_clouds = 75
# input_tempcel = 12
# input_weather_id = 500
# input_wind_speed = 11.32
# input_tempcel_feel = 11.42
# X_input = [[input_weather_main,input_clouds,input_tempcel, input_weather_id, input_wind_speed,input_tempcel_feel,input_month,input_day_of_week,input_hour]]



station_number = 10
model_park = load_model('park',station_number)
model_bike = load_model('bike',station_number)
if model_park is not None:
    predictions_park = []
    for X_web in weather_list:
        y_web = model_park.predict([X_web])
        predictions_park.append(int(y_web.round(0)))
    predictions_json_park = json.dumps(predictions_park)
    print(predictions_json_park)
else:
    print(f"Cannot find the park available model file for station number {station_number}")

if model_bike is not None:
    predictions_bike = []
    for X_web in weather_list:
        y_web = model_bike.predict([X_web])
        predictions_bike.append(int(y_web.round(0)))
    # Convert the predictions list to JSON format
    predictions_json_bike = json.dumps(predictions_bike)
    print(predictions_json_bike)
else:
    print(f"Cannot find the bike available model file for station number {station_number}")

