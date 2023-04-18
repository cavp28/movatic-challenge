from app.extensions import db
from app.api.models import StationInformation, StationStatus
from flask import json
from sqlalchemy import exc


# Return all stations.
# We can improve this by adding pagination, filters, etc.
def get_stations_information():
    return StationInformation.query.all()


# Return the status of an specific station.
def get_station_status(station_id):
    return StationStatus.query.get(station_id)


# Upsert station status and information
def upsert_station_status_and_information(status_list, information_list):
    # station_status_list = []
    # station_information_list = []

    ## THIS IS SUPER SLOW!
    # for status in status_list:
    #     try:
    #         db.session.merge(StationStatus(**status))
    #         db.session.commit()

    #     except exc.SQLAlchemyError:
    #         db.session.rollback()

    # for information in information_list:
    #     try:
    #         db.session.merge(StationInformation(**information))
    #         db.session.commit()
    #     except exc.SQLAlchemyError:
    #         db.session.rollback()
    try:
        db.session.bulk_insert_mappings(StationInformation, information_list)
        db.session.commit()
        db.session.bulk_insert_mappings(StationStatus, status_list)
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False
