from flask import jsonify, request, json
import requests
from app.api import bp
from app.api.controllers import get_stations_information, get_station_status, upsert_station_status_and_information
from app.api.serializers import station_status_serializer, station_information_serializer, station_information_deserializer, station_status_deserializer


@bp.route("/stations", methods=["GET"])
def list_stations():
    stations = get_stations_information()
    return jsonify(station_information_serializer.dump(stations, many=True)), 200

@bp.route("/stations/<station_id>/status", methods=['GET'])
def station_status(station_id):
    status = get_station_status(station_id)
    return jsonify(station_status_serializer.dump(station_status, many=False)), 200


@bp.route("/ingest", methods=['POST'])
def ingest():
    data = request.get_json()
    
    try:
        gbfs_url = data["gbfs_url"]
        try:
            response = requests.get(gbfs_url)
        except requests.ConnectionError:
            return "Connection Error"  
        
        data = json.loads(response.text)

        # Assuming that this will always be the same
        feeds = data["data"]["en"]["feeds"]

        # Adding two variables to store the urls for the resoureces that we will later consume
        station_information_url = None
        station_status_url = None

        # Since I don't know if the array will always be the same, let's itarate
        for feed in feeds:
            if feed["name"] == "station_information":
                station_information_url = feed["url"]
            
            if feed["name"] == "station_status":
                station_status_url = feed["url"]
            
            # If both exits, exit the loop.
            if station_information_url and station_status_url:
                break
        
        try:
            response = requests.get(station_information_url)
        except requests.ConnectionError:
            return "Connection Error"
        
        # This can be a function
        data = json.loads(response.text)

        stations = data["data"]["stations"]

        # Storing all stations here.
        station_information_list = []

        for station in stations:

            station_information_list.append({
                "station_id": station["station_id"],
                "address": station["address"],
                "latitude": station["latitude"],
                "longitude": station["longitude"]
            })

        try:
            response = requests.get(station_status_url)
        except requests.ConnectionError:
            return "Connection Error"
        
        # This can be a function
        data = json.loads(response.text)

        stations = data["data"]["stations"]

        # Storing all stations here.
        station_status_list = []

        for station in stations:

            station_status_list.append({
                "station_id": station["station_id"],
                "is_returning": station["is_returning"],
                "is_renting": station["is_renting"],
                "is_installed": station["is_installed"],
                "num_docks_available": station["num_docks_available"],
                "num_bikes_available": station["num_bikes_available"],
                "last_reported": station["last_reported"]
            })
        ## Now that we have the objets...
        
        status_list = station_status_deserializer.load(station_status_list, many=True)
        information_list = station_information_deserializer.load(station_information_list, many=True)

        upserted_data = upsert_station_status_and_information(status_list=status_list, information_list=information_list)
        
        return jsonify({
            "data_inserted_correctly": upserted_data
        }),  201
    
    except Exception as e:
       return jsonify({
            "error": e
        }),  500       

