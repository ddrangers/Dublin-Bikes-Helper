"""Declare mapped models and relationships."""
import datetime
import json

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, text, BINARY
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# # Create base object from sqlalchemy
# # Declarative Mapping, defines a Python object model, as well as database metadata that describes real SQL tables.
class Base(DeclarativeBase):
    pass

# ORM mapped classes
# Individual mapped classes(weatherInfo) are then created by making subclasses of Base
# The mapped class is any Python class we’d like to create, which will then have attributes on it that will be linked to the columns in a database table.
class weatherInfo(Base):
    # Table name
    __tablename__ = "weather_info"
    # Define table field (the mapped_column() construct in combination with typing annotations will generate Column objects)
    id: Mapped[str] = mapped_column(String, primary_key=True)   # To indicate columns in the Table, use the mapped_column() construct
    coord_lon: Mapped[str] = mapped_column(String(20))  # "Mapped[]" will be filled with python data types
    coord_lat: Mapped[str] = mapped_column(String(20))  # "mapped_column()" will be filled with alchemy types
    weather_id: Mapped[int] = mapped_column()
    weather_main: Mapped[str] = mapped_column(String(20))
    temp: Mapped[float] = mapped_column(Float)
    temp_feel: Mapped[float] = mapped_column(Float)
    wind_speed: Mapped[float] = mapped_column(Float)
    clouds: Mapped[int] = mapped_column()
    sunrise: Mapped[datetime] = mapped_column(DateTime)
    sunset: Mapped[datetime] = mapped_column(DateTime)
    creat_time: Mapped[datetime] = mapped_column(DateTime)
    delete_flag: Mapped[int] = mapped_column(DateTime)



# reading the config file to construct engine
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
# The Engine is a factory that can create new database connections for us, which also holds onto connections in Connection Pool for fast reuse.
engine = create_engine(connection_string, echo=True)

# Before insert data into the mysql. make sure the database are created in the DB
# generate our schema (PRAGMA statements are run, but no new tables are generated since they are found to be present already)
Base.metadata.create_all(engine)