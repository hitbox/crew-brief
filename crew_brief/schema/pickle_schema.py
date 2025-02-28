import marshmallow as mm

from .user_events_schema import UserEventsSchema

class PickleSchema(mm.Schema):
    """
    Structure of the data stored in the pickle database.
    """

    member_data = mm.fields.Nested(
        UserEventsSchema,
        # Some zips didn't have the member we wanted.
        missing = None,
        metadata = dict(
            description = 'JSON data from the matching member file.',
        ),
    )

    path = mm.fields.String(
        required = True,
        metadata = dict(
            description = 'Path to ZIP.',
        ),
    )

    path_data = mm.fields.Dict(
        required = True,
        metadata = dict(
            description = 'Data parsed from the path.',
        ),
    )
