import requests
import json
import uuid
import  models
import sqlalchemy

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, text, BINARY, inspect
from sqlalchemy.orm import Session

import schedule
import time


def get_weather():
    print('this is the scraping data process!!!')
    # ------------------------------------- Weather scraping task using OpenweatherAPI -------------------------------------
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
    weather_Json = json.loads(response_weather)  # Convert from JSON to Python
    json_str = json.dumps(weather_Json, indent=3)  # convert from python to json
    # inspect the downloaded json file
    # print(json_str)

    # ------------------------------------- store the weather information into database ------------------------------------
    # ------------ 1. Connect to the database in RDS and testing------------
    # reading the config file to construct SQL alchemy engine
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
    # Before insert data into the mysql. make sure the database are created in the DB
    # generate our schema (PRAGMA statements are run, but no new tables are generated since they are found to be present already)
    models.Base.metadata.create_all(engine)

    # check the sqlalchemy version
    print("The sqlalchemy version installed is:", sqlalchemy.__version__)

    # test the connection to the database
    try:
        inspectObj = inspect(engine)
        print("The mysql database name in AWS:", inspectObj.get_table_names())
    except Exception as e:
        print(e)

    # Mysql alchemy - core: test retrieve a row of data
    mysqlTestRequest = text(
        "SELECT id, coord_lat, coord_lon, weather_id, weather_main, creat_time  FROM weather_info WHERE weather_info.weather_id = '803'")
    try:
        with Session(engine) as session:
            result = session.execute(mysqlTestRequest)
            for row in result:
                print("-------------------testing: The retrieved weather_id is", row.weather_id, "------------------------")
    except Exception as e:
        print(e)


    # ------------------------ 2. initialize SQLAlchemy DB-Session and insert the data to mysql ----------------------------
    # Parse the weather JSON file
    coord_lon = weather_Json["coord"]["lon"]
    coord_lat = weather_Json["coord"]["lat"]
    weather_id = weather_Json["weather"][0]["id"]
    weather_main = weather_Json["weather"][0]["main"]
    temp = weather_Json["main"]["temp"]
    temp_feel = weather_Json["main"]["feels_like"]
    wind_speed = weather_Json["wind"]["speed"]
    clouds = weather_Json["clouds"]["all"]
    sunriseUTC = weather_Json["sys"]["sunrise"]
    sunsetUTC = weather_Json["sys"]["sunset"]
    delete_flag = 0

    # init process of the raw data
    sunriseTime = datetime.fromtimestamp(sunriseUTC)
    sunsetTime = datetime.fromtimestamp(sunsetUTC)
    print("test:", sunsetTime)


    # Generate the id for the weather data
    uuid_bytes = uuid.uuid4().bytes[:16]   # Generate a UUID with 16 bytes of string
    uuid_string = uuid.UUID(bytes=uuid_bytes).hex  # Convert the UUID to a string

    # insert the weather data into the DB
    try:
        with Session(engine) as session:
            insertWeather = models.weatherInfo(
                id=uuid_string,
                coord_lon=coord_lon,
                coord_lat=coord_lat,
                weather_id=weather_id,
                weather_main=weather_main,
                temp=temp,
                temp_feel=temp_feel,
                wind_speed=wind_speed,
                clouds=clouds,
                sunrise=sunriseTime,
                sunset=sunsetTime,
                creat_time=datetime.now(),
                delete_flag=0,
            )
            session.add(insertWeather)
            session.commit()
    except Exception as e:
        print(e)



def run_task():
    # Set daily scheduled tasks.
    schedule.every(1).minutes.do(get_weather)
    # Infinite loop, automatically run scheduled tasks in the background
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start a scheduled task
run_task()