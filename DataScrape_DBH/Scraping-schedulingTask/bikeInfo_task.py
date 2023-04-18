import requests
import json
import uuid
import models
import schedule
import time

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, text, BINARY, inspect
from sqlalchemy.orm import Session



def get_bike():
    # ------------------------------------------- Bike scraping task using -----------------------------------------------
    # restructured to python file from (Datascrap_bike_realtime.ipynb)

    dub_bike_response = requests.get('https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=004cf9dced9bc8d383db556938be65d9449aeae2')
    print("Bike API response code:", dub_bike_response.status_code)

    # read the scraping json file
    response_bike = dub_bike_response.text
    bike_jsonObj = json.loads(response_bike)

    # inspect the downloaded json file
    print(json.dumps(bike_jsonObj, indent=3))  # convert from json to python to print

    # --------------------------------------------------- Data insertion ---------------------------------------------------
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

    # MYSQL insertion
    for j in range(len(bike_jsonObj)):
        # Parse the weather JSON file
        number = bike_jsonObj[j]["number"]
        name = bike_jsonObj[j]["name"]
        address = bike_jsonObj[j]["address"]
        bike_stand = bike_jsonObj[j]["bike_stands"]
        bike_stand_available = bike_jsonObj[j]["available_bike_stands"]
        bike_available = bike_jsonObj[j]["available_bikes"]
        status = bike_jsonObj[j]["status"]
        last_update = bike_jsonObj[j]["last_update"]
        # init process of the raw data

        last_update=int(str(last_update)[:10])
        print(last_update)

        last_update = datetime.fromtimestamp(last_update)
        # Generate the id for the weather data
        uuid_bytes = uuid.uuid4().bytes[:16]  # Generate a UUID with 16 bytes of string
        uuid_string = uuid.UUID(bytes=uuid_bytes).hex  # Convert the UUID to a string
        # set the initial value
        creat_time = datetime.now()
        delete_flag = 0
        try:
            with Session(engine) as session:
                insertBikeInfo = models.bikeInfo(
                    id=uuid_string,
                    number=number,
                    name=name,
                    address=address,
                    bike_stand=bike_stand,
                    bike_stand_available=bike_stand_available,
                    bike_available = bike_available,
                    status = status,
                    last_update = last_update,
                    creat_time=creat_time,
                    delete_flag=delete_flag,
                )
                session.add(insertBikeInfo)
                session.commit()
        except Exception as e:
            print(e)



def run_task():
    # Set daily scheduled tasks.
    schedule.every(1).minutes.do(get_bike)
    # Infinite loop, automatically run scheduled tasks in the background
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start a scheduled task
run_task()

