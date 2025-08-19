from marshmallow import Schema
from marshmallow.fields import Date
from marshmallow.fields import DateTime
from marshmallow.fields import String

from .field import IsPreflight
from .field import ofp_version_field

class CrewBriefArchiveSchema(Schema):
    """
    Crew Brief ZIP filename schema.
    """

    folder_date = Date()
    airline_iata = String()
    flight_number = String()
    origin_date = Date(format='%d%b%y')
    departure_iata = String()
    destination_iata = String()
    ofp_version = ofp_version_field('_')
    datetime = DateTime(format='%d%b%Y%H%M%S')
    is_preflight = IsPreflight()
