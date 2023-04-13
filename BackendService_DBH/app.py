import json
import requests
from flask import Flask, jsonify
from sqlalchemy import create_engine, select, MetaData, Table, text
import pandas as pd
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)

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
    # get db connection
    return "list of stations"
    bike_response = requests.get(
        'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=004cf9dced9bc8d383db556938be65d9449aeae2')
    if bike_response.status_code == 200:
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


