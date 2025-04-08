import datetime

from operator import itemgetter

import marshmallow as mm

from file_zipper import utils

from .base import BaseSchema
from .field import TransformDateField
from .field import TransformDateTimeField
from .mixin import OrderMixin
from .mixin import ValidateMixin

class PDFPathUnderscoreSchema(BaseSchema, OrderMixin, ValidateMixin):
    """
    PDF path data schema.
    """

    airline_iata1 = mm.fields.String()
    dir_date = mm.fields.Date(format='%Y-%m-%d')
    airline_iata2 = mm.fields.String()
    flight_number = mm.fields.String()

    flight_date_month_name = mm.fields.String(data_key='flight_date_month')
    flight_date_month_int = mm.fields.Integer()
    flight_date_day = mm.fields.Integer()

    origin_iata = mm.fields.String()
    destination_iata = mm.fields.String()
    dispatcher = mm.fields.String()
    datetime1 = TransformDateTimeField(load_format='%Y%m%d%H%M%S')
    datetime2 = TransformDateTimeField(load_format='%Y%m%d%H%M%S')

    # Ordered applied by OrderMixin
    _preferred_order = [
        'airline_iata1',
        'airline_iata2',
        'flight_number',
        'origin_iata',
        'destination_iata',
        'datetime1',
        'datetime2',
        'dir_date',
        'dispatcher',
        'flight_date_month',
        'flight_date_month_name',
        'flight_date_month_int',
        'flight_date_day',
    ]

    @mm.pre_load
    def convert_flight_date_month_name(self, data, **kwargs):
        """
        Convert and add flight date month name to integer.
        """
        # Add integer month for flight.
        data['flight_date_month_int'] = utils.abbr_month_int(data['flight_date_month'])
        return data


class PDFPathSpaceSchema(BaseSchema, OrderMixin, ValidateMixin):
    """
    PDF path data schema.
    """

    airline_iata1 = mm.fields.String()
    dir_date = mm.fields.Date(format='%Y-%m-%d')
    airline_iata2 = mm.fields.String()
    flight_number = mm.fields.String()
    flight_date = TransformDateField(load_format='%d%b%y')
    origin_iata = mm.fields.String()
    destination_iata = mm.fields.String()
    ofp_revision_major = mm.fields.Integer()
    ofp_revision_minor = mm.fields.Integer()
    ofp_revision_patch = mm.fields.Integer()

    # Ordered applied by OrderMixin
    _preferred_order = [
        'airline_iata1',
        'airline_iata2',
        'flight_date',
        'flight_number',
        'origin_iata',
        'destination_iata',
        'dir_date',
    ]
