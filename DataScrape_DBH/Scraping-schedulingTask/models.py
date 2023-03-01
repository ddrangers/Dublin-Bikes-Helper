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


class bikeInfo(Base):
    __tablename__ = "bike_info"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    number: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(40))
    address: Mapped[str] = mapped_column(String(40))
    bike_stand: Mapped[int] = mapped_column()
    bike_stand_available: Mapped[int] = mapped_column()
    bike_available: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(40))
    last_update: Mapped[datetime] = mapped_column(DateTime)
    creat_time: Mapped[datetime] = mapped_column(DateTime)
    delete_flag: Mapped[int] = mapped_column(DateTime)



class bikeStatic(Base):
    __tablename__ = "bike_static"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    indexNumber: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(40))
    address: Mapped[str] = mapped_column(String(40))
    location_lat: Mapped[float] = mapped_column()
    location_lon: Mapped[float] = mapped_column()
    creat_time: Mapped[datetime] = mapped_column(DateTime)
    delete_flag: Mapped[int] = mapped_column(DateTime)