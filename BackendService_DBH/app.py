import json
import requests
from flask import Flask, jsonify
from sqlalchemy import create_engine, select, MetaData, Table, text
import pandas as pd
import pickle
import os
import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/stations')
def index():
    # get db connection
    # engine = create_engine('postgresql://masterAdmin:4hvJWtw1P4cV7Xm0JQno@database-ddrangers.cftjf3yfdzfx.eu-west-1.rds.amazonaws.com:3306/bike_static_test')
    with open("config.json", "r") as jsonfile:
        configFile = json.load(jsonfile)
        print("successfully loading Json config file...")
    print("reading config file:", configFile)
    username = configFile['username']
    password = configFile['password']
    host = configFile['host']
    port = configFile['port']
    database_name = configFile['database_name']
    # assemble the connection string
    connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
    # # The Engine is a factory that can create new database connections for us, which also holds onto connections in Connection Pool for fast reuse.
    engine = create_engine(connection_string, echo=True)
    # creat database object
    metadata = MetaData()
    bike_static = Table('bike_static', metadata, autoload_with=engine)

    # # the column we need
    # columns = ['indexNumber', 'name', 'address', 'location_lat', 'location_lon']
    #
    # # query the data for specified columns
    # stmt = select([getattr(bike_static_test.c, column) for column in columns])
    sql1 = "SELECT a.indexNumber, a.name, a.location_lat, a.location_lon FROM bike_static as a;"

    stmt = select(
        bike_static.c.indexNumber,
        bike_static.c.name,
        bike_static.c.address,
        bike_static.c.location_lat,
        bike_static.c.location_lon
    )

    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

    print("------------------------------------------")
    sql = text(sql1)
    df = pd.read_sql(sql, con=engine.connect())
    print(df)
    return df.to_json(orient="records")


@app.route('/weather')
def weather():
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
    # print(weather_result)
    return weather_result


@app.route('/stationsPredict/<int:current_bike_station_id>')
def stationsPredict(current_bike_station_id):
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

    model_park = load_model('park', current_bike_station_id)
    model_bike = load_model('bike', current_bike_station_id)
    if model_park is not None and model_bike is not None:
        predictions_park = []
        predictions_bike = []

        for X_web in weather_list:
            y_web_park = model_park.predict([X_web])
            predictions_park.append(int(y_web_park.round(0)))

            y_web_bike = model_bike.predict([X_web])
            predictions_bike.append(int(y_web_bike.round(0)))

        if model_park is None:
            predictions_park = 'Cannot find the park available model file for station number {current_bike_station_id}'
        if model_bike is None:
            predictions_bike = "Cannot find the bike available model file for station number {current_bike_station_id}"

        # Create a dictionary with both predictions
        predictions_dict = {
            'park_predictions': predictions_park,
            'bike_predictions': predictions_bike
        }
        # Convert the dictionary to JSON format
        predictions_json = json.dumps(predictions_dict)
        return predictions_json





@app.route('/stations/<int:indexnumber>')
def station(indexnumber):
    dub_bike_response = requests.get(
        'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=004cf9dced9bc8d383db556938be65d9449aeae2')
    if dub_bike_response.status_code == 200:
        print('work')
        bike_json = json.loads(dub_bike_response.text)
        for station in bike_json:
            if station['number'] == indexnumber:
                # Extract the required fields for the station
                index = station['number']
                name = station['name']
                address = station['address']
                bike_stand = station['bike_stands']
                bike_stand_available = station['available_bike_stands']
                bike_available = station['available_bikes']
                status = station['status']

                # Create a dictionary to store the extracted data
                data = {
                    "index": index,
                    "name": name,
                    "address": address,
                    "bike_stand": bike_stand,
                    "bike_stand_available": bike_stand_available,
                    "bike_available": bike_available,
                    "status": status
                }

                # Convert the dictionary to JSON and return the result #in fuction add return
                station_result = json.dumps(data, indent=3)  # # Convert the dictionary to JSON
                return station_result
            # Return an error message if the station ID is not found
        data = "error: Station not found"
        station_result = json.dumps(data, indent=3)
        return station_result


if __name__ == '__main__':
    app.run(debug=True)


