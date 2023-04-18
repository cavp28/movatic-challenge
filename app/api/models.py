from app.extensions import db
import datetime
import uuid


class StationInformation(db.Model):
    # __tablename__ = 'information'
    station_id = db.Column(db.String(100), primary_key=True, nullable=False)
    id = db.Column(db.String(36), default=uuid.uuid4)
    address = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # Adding a relationship between Station and Station Status
    # station_status = db.relationship('Station_Status', backref='station_information', lazy=True,
    #                          primaryjoin='Station_Information.station_id == Station_Status.station_id')

    def __init__(self, station_id, address, latitude, longitude):
        self.station_id = station_id
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def json(self):
        return {
            "station_id": self.station_id,
            "address": self.address,
            "self.latitude": self.latitude,
            "self.longitude": self.longitude,
        }


class StationStatus(db.Model):
    # __tablename__ = 'status'
    station_id = db.Column(db.String(100), primary_key=True, nullable=False)
    id = db.Column(db.String(36), default=uuid.uuid4)
    is_returning = db.Column(db.Boolean, nullable=False, default=False)
    is_renting = db.Column(db.Boolean, nullable=False, default=False)
    is_installed = db.Column(db.Boolean, nullable=False, default=False)
    num_docks_available = db.Column(db.Integer, nullable=False, default=0)
    num_bikes_available = db.Column(db.Integer, nullable=False)
    # If we look here https://github.com/MobilityData/gbfs-json-schema/blob/master/v3.0-RC/station_status.json
    # they say that this it comes as an integer, but I will use it cast it to DataTime, like the requirements says
    last_reported = db.Column(db.DateTime, nullable=False)
    # station = db.Column(db.String(36), db.ForeignKey('station_information.station_id'), nullable=False)

    def __init__(
        self,
        station_id,
        is_returning,
        is_renting,
        is_installed,
        num_docks_available,
        num_bikes_available,
        last_reported,
    ):
        self.station_id = station_id
        self.is_returning = is_returning
        self.is_renting = is_renting
        self.is_installed = is_installed
        self.num_docks_available = num_docks_available
        self.num_bikes_available = num_bikes_available
        self.last_reported = last_reported
        # self.station = station_id

    def json(self):
        return {
            "station_id": self.station_id,
            "is_returning": self.is_returning,
            "is_renting ": self.is_renting,
            "is_installed": self.is_installed,
            "num_docks_available": self.num_docks_available,
            "num_bikes_available": self.num_bikes_available,
            "last_reported": self.last_reported,
        }
