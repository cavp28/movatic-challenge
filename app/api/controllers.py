from app.extensions import db
from app.api.models import Station_Information, Station_Status
from flask import json
from sqlalchemy import exc

# Return all stations.
# We can improve this by adding pagination, filters, etc.
def get_stations_information():
    return Station_Information.query.all()

# Return the status of an specific station.
def get_station_status(station_id):
    status = Station_Status.query.get(station_id)
    return json.dumps(status.json())

# Upsert station status and information
def upsert_station_status_and_information(status_list, information_list):
    station_status_list = []
    station_information_list = []
    
    for status in status_list:
        station_status_list.append(Station_Status(**status))
    
    for information in information_list:
        station_information_list.append(Station_Information(**information))

    
    try:
        db.session.bulk_save_objects(station_information_list)
        db.session.commit()
        db.session.bulk_save_objects(station_status_list)
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False