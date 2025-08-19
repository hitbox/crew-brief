from marshmallow import Schema
from marshmallow.fields import Date
from marshmallow.fields import DateTime
from marshmallow.fields import String

from .constant import COMPACT_FMT
from .field import ofp_version_field

class LCBArchiveSchema(Schema):

    folder_date = Date()

    airline_icao = String()
    airline_iata = String()
    airline_iata2 = String()

    short_date = Date(format='%b%y')

    flight_number = String()
    origin_date = Date(
        format = '%d%b%y', # Short date format from inside PDF.
    )
    departure_iata = String()
    destination_iata = String()

    dispatcher_firstlast = String()

    scheduled_departure_datetime = DateTime(
        format = COMPACT_FMT,
    )

    lido_weather_service_datetime = DateTime(
        format = COMPACT_FMT,
    )

    aircraft_registration = String()

    ofp_version = ofp_version_field('/')

    filename_suffix = String()

    origin_date_month_day = String()
