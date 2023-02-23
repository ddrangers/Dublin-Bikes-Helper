import requests
import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, text, BINARY, inspect
from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy.orm import Session



# ---------------------------- Weather scraping task using OpenweatherAPI ---------------------------------
# Get the coordinate of Dublin city from Geocoding API
token = "06070e53f0b195fef92272b71f2c0963"
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
response_rawWeather = requests.get(url)

# check the response status
response_statusCode2 = response_rawWeather.status_code
print(response_statusCode2)  # return 200 means OK

# Get the weather JSON data
response_weather = response_rawWeather.text
weather_Json = json.loads(response_weather)
json_str = json.dumps(weather_Json, indent=3)
# inspect the downloaded json file
# print(json_str)

# ---------------------------- store the weather information into database ---------------------------------

# ------------ 1. Establish SQLAlchemy to AWS Connection ------------

# specify the connection parameters
# TODO: move the connection info to the config file
username = 'masterAdmin'
password = '4hvJWtw1P4cV7Xm0JQno'
host = 'database-ddrangers.cftjf3yfdzfx.eu-west-1.rds.amazonaws.com'
port = 3306
database_name = 'DBH_schema'

# initializing DB connection ("'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'")
# create the connection string:  mysql+pymysql://<username>:<password>@<host>/<database_name>
connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'

# create the engine (Engine can create new database connections, which holds the connections in Connection Pool
engine = create_engine(connection_string, echo=True)

# check the sqlalchemy version
print("The sqlalchemy version installed is:", sqlalchemy.__version__)

# test the connection to the database
inspectObj = inspect(engine)
print("The mysql database name in AWS:", inspectObj.get_table_names())

# test retrieve a row of data
mysqlRequest = text("SELECT id, coord_lat, coord_lon, weather_id, weather_main, creat_time  FROM weather_info WHERE weather_info.weather_id = '803'")
with Session(engine) as session:
    result = session.execute(mysqlRequest)
    for row in result:
        print("the retrieved weather_id is", row.weather_id)














# # ------------ 2. initialize SQLAlchemy DB-Session and define each table's field ------------
#
# # Create base object from sqlalchemy
# # Declarative Mapping, defines a Python object model, as well as database metadata that describes real SQL tables.
# class Base(DeclarativeBase):  # acquire a new Declarative Base which subclasses the SQLAlchemy DeclarativeBase class
#     pass
#
#
# # Individual mapped classes(weatherInfo) are then created by making subclasses of Base
# # The mapped class is any Python class we’d like to create, which will then have attributes on it that will be linked to the columns in a database table.
# class WeatherInfo(Base):
#     # Table name
#     __tablename__ = "weather_info"
#
#     # Define table field
#     id: Mapped[BINARY(16)] = mapped_column(primary_key=True)   # To indicate columns in the Table, use the mapped_column() construct
#     coord_lon: Mapped[str] = mapped_column(String(20))
#     coord_lat: Mapped[str] = mapped_column(String(20))
#     weather_id: Mapped[int] = mapped_column()
#     weather_main: Mapped[int] = mapped_column(String(20))
#     temp: Mapped[float] = mapped_column(Float)
#     temp_feel: Mapped[float] = mapped_column(Float)
#     wind_speed: Mapped[float] = mapped_column(Float)
#     clouds: Mapped[int] = mapped_column()
#     sunrise: Mapped[DateTime] = relationship()
#     sunset: Mapped[DateTime] = relationship()
#     creat_time: Mapped[DateTime] = relationship()
#     delete_flag: Mapped[Boolean] = relationship()
#
#
#
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)
#
# # ------------ 3. after creating engine and sessionMaker, add the data to the database ---------------
# # get the session, add the object in the session, commit and close the session.
#
# # test: query to aws rds
# # 创建session对象:
# session = DBSession()
# # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
# weatherInfo = session.query(WeatherInfo).one()
# # 打印类型和对象的name属性:
# print('temp:', WeatherInfo.temp)
# # 关闭Session:
# session.close()
# #
# # # # Add the weather json data to the mysql database
# # # # creat session:
# # # session = DBSession()
# # # # creat weather info obj:
# # # new_weatherInfo = weatherInfo(id='5', name='Bob')
# # # # add the obj to session:
# # # session.add(new_weatherInfo)
# # # # commit the change to the RDS AWS:
# # # session.commit()
# # # # close the session:
# # # session.close()
