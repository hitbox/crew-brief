import marshmallow as mm

class BaseSchema(mm.Schema):

    airline_iata1 = mm.fields.String(allow_none=True, load_default=None)
    airline_iata2 = mm.fields.String(allow_none=True, load_default=None)
    flight_date = mm.fields.DateTime(allow_none=True, load_default=None)
    flight_number = mm.fields.String(allow_none=True, load_default=None)
    origin_iata = mm.fields.String(allow_none=True, load_default=None)
    destination_iata = mm.fields.String(allow_none=True, load_default=None)

    ofp_revision_major = mm.fields.Integer(allow_none=True, load_default=None)
    ofp_revision_minor = mm.fields.Integer(allow_none=True, load_default=None)
    ofp_revision_patch = mm.fields.Integer(allow_none=True, load_default=None)

    datetime1 = mm.fields.DateTime(allow_none=True, load_default=None)
    datetime2 = mm.fields.DateTime(allow_none=True, load_default=None)
    dir_date = mm.fields.Date(allow_none=True, load_default=None)
    dispatcher = mm.fields.String(allow_none=True, load_default=None)
    flight_date_day = mm.fields.Integer(allow_none=True, load_default=None)
    flight_date_month_int = mm.fields.Integer(allow_none=True, load_default=None)
    flight_date_month_name = mm.fields.String(allow_none=True, load_default=None)
