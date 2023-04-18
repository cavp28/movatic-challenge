from flask import request, json
import requests
from app.api import bp
from app.api.controllers import (
    get_stations_information,
    get_station_status,
    upsert_station_status_and_information,
)
from app.api.serializers import (
    station_status_serializer,
    station_information_serializer,
    station_information_deserializer,
    station_status_deserializer,
)
import datetime


@bp.route("/", methods=["GET","POST"])
def index():
    return (
            json.dumps({"success": True, "message": "App running! :D"}),
            500,
            {"ContentType": "application/json"},
        )

# TODO: Add pagination if there's time.
@bp.route("/stations", methods=["GET"])
def list_stations():
    stations = get_stations_information()
    return (
        json.dumps(station_information_serializer.dump(stations, many=True)),
        200,
        {"ContentType": "application/json"},
    )


@bp.route("/stations/<station_id>/status", methods=["GET"])
def station_status(station_id):
    status = get_station_status(station_id)
    if status:
        return (
            json.dumps(station_status_serializer.dump(status)),
            200,
            {"ContentType": "application/json"},
        )
    else:
        return (
            json.dumps({"success": False, "error": f"{station_id} station not found"}),
            404,
            {"ContentType": "application/json"},
        )


# TODO: Improve this function, specifically the part when querying the data.
@bp.route("/ingest", methods=["POST"])
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
            station_information_list.append(
                {
                    "station_id": station["station_id"],
                    "address": station["address"],
                    "latitude": station["lat"],
                    "longitude": station["lon"],
                }
            )

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
            # Make sure to cast to boolean the integer values
            station_status_list.append(
                {
                    "station_id": station["station_id"],
                    "is_returning": bool(station["is_returning"]),
                    "is_renting": bool(station["is_renting"]),
                    "is_installed": bool(station["is_installed"]),
                    "num_docks_available": int(station["num_docks_available"]),
                    "num_bikes_available": int(station["num_bikes_available"]),
                    "last_reported": datetime.datetime.fromtimestamp(
                        station["last_reported"]
                    ).strftime("%Y-%m-%dT%H:%M:%SZ"),
                }
            )
        ## Now that we have the objets...

        deserialized_status_list = [
            station_status_deserializer.load(st_status)
            for st_status in station_status_list
        ]

        deserialized_information_list = [
            station_information_deserializer.load(st_information)
            for st_information in station_information_list
        ]

        upserted_data = upsert_station_status_and_information(
            status_list=deserialized_status_list,
            information_list=deserialized_information_list,
        )
        if upserted_data:
            return (
                json.dumps(
                    {
                        "success": upserted_data,
                        "info": f"{len(deserialized_status_list)} status were upserted. {len(deserialized_information_list)} station information were upserted",
                    }
                ),
                200,
                {"ContentType": "application/json"},
            )
        else:
            return (
                json.dumps(
                    {"success": upserted_data, "error": "Issues upserting the data"}
                ),
                500,
                {"ContentType": "application/json"},
            )

    except Exception as e:
        return (
            json.dumps({"success": False, "error": f"{e}"}),
            500,
            {"ContentType": "application/json"},
        )
