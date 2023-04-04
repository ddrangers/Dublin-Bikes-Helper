import json
import requests
from flask import Flask
from sqlalchemy import create_engine, select, MetaData, Table
app = Flask(__name__)


@app.route('/')
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

    stmt = select(
        bike_static.c.indexNumber,
        bike_static.c.name,
        bike_static.c.address,
        bike_static.c.location_lat,
        bike_static.c.location_lon
    )

    # execute the query and get result
    with engine.connect() as conn:
        results = conn.execute(stmt).fetchall()

    # turn the format of result to json
    json_results = json.dumps([dict(row) for row in results])

    return json_results


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
        "temp": temp,
        "temp_feel": temp_feel,
        "wind_speed": wind_speed
    }

    weather_result = json.dumps(data, indent=3)  # # Convert the dictionary to JSON
    # print(weather_result)
    return weather_result


@app.route('/stations')
def stations():
    # get db connection
    return "list of stations"


@app.route('/stations/<int:station_id>')
def station(station_id):
    # show the station with the given id, the id is an integer
    return 'Retrieving info for Station: {}'.format(station_id)
