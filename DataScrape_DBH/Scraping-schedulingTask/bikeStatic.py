import pandas as pd
import json
import csv
import uuid
import  models
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, text, BINARY, inspect


# Note: The bike static file will only be used for import into mysql database for one time.
# -------------------------------- read the local csv file and transform to a JSON file ---------------------------------

# read the csv file
df = pd.read_csv("dublin1_static.csv")
print("Static bike data shape: ", df.shape)
print(df.head(3))
print(df.tail(3))

# Read CSV file and create a list of dictionaries
csv_list = []
with open("dublin1_static.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        csv_list.append(row)

# Convert list of dictionaries to JSON object
json_object = json.dumps(csv_list, indent=2)
# Print the JSON object
print(json_object)

# ------------------------------------------ Move the entire JSON file to database -----------------------------------
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


# proces the data in JSON file
json_bike = json.loads(json_object)
dict_length = len(json_bike)
print("The json file length:", dict_length)

for j in range(dict_length):
    # Parse a single JSON file
    indexNumber = json_bike[j]["Number"]
    name = json_bike[j]["Name"]
    address = json_bike[j]["Address"]
    location_lat = json_bike[j]["Latitude"]
    location_lon = json_bike[j]["Longitude"]
    # get the current time to insert into the DB and init set the delete column
    now = datetime.now()
    delete_flag = 0
    # Generate the id for the weather data
    uuid_bytes = uuid.uuid4().bytes[:16]   # Generate a UUID with 16 bytes of string
    uuid_string = uuid.UUID(bytes=uuid_bytes).hex  # Convert the UUID to a string
    # insert the weather data into the DB
    try:
        with Session(engine) as session:
            insertBikeStatic = models.bikeStatic(
                id=uuid_string,
                indexNumber=indexNumber,
                name=name,
                address=address,
                location_lat=location_lat,
                location_lon=location_lon,
                creat_time=now,
                delete_flag=0,
            )
            session.add(insertBikeStatic)
            session.commit()
    except Exception as e:
        print(e)


