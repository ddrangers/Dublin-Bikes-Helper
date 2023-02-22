import requests
import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, text, BINARY, inspect


# ----------------------- Weather scraping task using OpenweatherAPI ----------------------------
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
# print(json_str)

# ----------------------- store the weather information into database ----------------------------

# 1. initialize SQLAlchemy DB-Session and define each table's field

# # Create base object from sqlalchemy
# Base = declarative_base()
# class weatherInfo(Base):
#     # Table name
#     __tablename__ = 'weather_info'
#     # Table field
#     id = Column(BINARY(16), primary_key=True)
#     coord_lon = Column(String(20))
#     coord_lat = Column(String(20))
#     weather_id = Column(Integer)
#     weather_main = Column(String(20))
#     temp = Column(Float)
#     temp_feel = Column(Float)
#     wind_speed = Column(Float)
#     clouds = Column(Integer)
#     sunrise = Column(DateTime)
#     sunset = Column(DateTime)
#     creat_time = Column(DateTime)
#     delete_flag = Column(Boolean)


# initializing DB connection ("'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'")
# mysql+pymysql://<username>:<password>@<host>/<database_name>

# engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
# # Create DBSession type
# DBSession = sessionmaker(bind=engine)


# specify the connection parameters
username = 'masterAdmin'
password = '4hvJWtw1P4cV7Xm0JQno'
host = 'database-ddrangers.cftjf3yfdzfx.eu-west-1.rds.amazonaws.com'
port = 3306
database_name = 'DBH_schema'

# create the connection string
connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'

# create the engine object
engine = create_engine(connection_string)

# test the connection to the database
insp = inspect(engine)
print("The mysql database name in AWS:", insp.get_table_names())












# # ------------ after creating engine and sessionMaker, add the data to the database ---------------
# # get the session, add the object in the session, commit and close the session.
#
# # 创建session对象:
# session = DBSession()
# # 创建新User对象:
# new_user = weatherInfo(id='5', name='Bob')
# # 添加到session:
# session.add(new_user)
# # 提交即保存到数据库:
# session.commit()
# # 关闭session:
# session.close()




