import marshmallow as mm

from .base import BaseSchema
from .field import TransformDateField
from .field import TransformDateTimeField
from .mixin import OrderMixin
from .mixin import ValidateMixin

class ZipPathSchema(BaseSchema, OrderMixin, ValidateMixin):
    """
    ZIP path data schema.
    """

    airline_iata1 = mm.fields.String()
    airline_iata2 = mm.fields.String()
    directory_date = mm.fields.Date(format='%Y-%m-%d')
    airline_iata3 = mm.fields.String()
    flight_number = mm.fields.String()

    flight_date = TransformDateField(load_format='%d%b%y')

    origin_iata = mm.fields.String()
    destination_iata = mm.fields.String()
    revision_major = mm.fields.Integer()
    revision_minor = mm.fields.Integer()
    revision_patch = mm.fields.Integer()

    departure_datetime = TransformDateTimeField(
        load_format = '%d%b%Y%H%M%S',
        dump_format = '%Y-%m-%dT%H:%M:%S',
    )

    preflight = mm.fields.String(load_default=None)

    # Order applied by OrderMixin
    _preferred_order = [
        'airline_iata1',
        'airline_iata2',
        'airline_iata3',
        'flight_date',
        'flight_number',
        'origin_iata',
        'departure_datetime',
        'destination_iata',
        'revision_major',
        'revision_minor',
        'revision_patch',
        'directory_date',
        'preflight',
    ]
