from marshmallow import Schema, fields

class StationInformationSchema(Schema):
    id = fields.String(dump_only=True)
    station_id = fields.String(required=True)
    address = fields.String()
    latitude = fields.Float()
    longitude = fields.Float()

class StationStatusSchema(Schema):
    id = fields.String(dump_only=True)
    station_id = fields.String(required=True)
    is_returning = fields.Boolean()
    is_renting = fields.Boolean()
    is_installed = fields.Boolean()
    num_docks_available = fields.Integer()
    num_bikes_available = fields.Integer()
    last_reported = fields.DateTime()


station_information_serializer = StationInformationSchema()
station_information_deserializer = StationInformationSchema(exclude=('id',))

station_status_serializer = StationStatusSchema()
station_status_deserializer = StationStatusSchema(exclude=('id',))
