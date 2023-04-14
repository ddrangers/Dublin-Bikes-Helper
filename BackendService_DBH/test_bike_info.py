import json
import requests
from flask import jsonify


# Get the station information for the given ID
dub_bike_response = requests.get(
            'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=004cf9dced9bc8d383db556938be65d9449aeae2')
station_id = 42
if dub_bike_response.status_code == 200:
    print('work')
    bike_json = json.loads(dub_bike_response.text)
    for station in bike_json:
        if station['number'] == station_id:
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
            print(data)

        # Return an error message if the station ID is not found
    print('("error": "Station not found")')

