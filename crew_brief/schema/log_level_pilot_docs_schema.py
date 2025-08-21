from marshmallow import Schema
from marshmallow.fields import Date
from marshmallow.fields import DateTime
from marshmallow.fields import String

from .field import IsPreflight
from .field import ofp_version_field

class LogLevelPilotDocsSchema(Schema):

    folder_date = Date(format='%Y_%m_%d')

    airline_icao = String()
    airline_iata = String()

    unknown = String()
    unknown1 = String()
    folder_date2 = Date()

    flight_number = String()
    origin_date = Date()
    departure_iata = String()
    destination_iata = String()
    ofp_version = ofp_version_field('_')
    datetime = DateTime(format='%d%b%Y%H%M%S')
    is_preflight = IsPreflight()

    filename_suffix = String()

    short_description = String(allow_none=True)
