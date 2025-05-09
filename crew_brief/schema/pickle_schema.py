import marshmallow as mm

from .user_event import UserEventsFileSchema

class PickleSchema(mm.Schema):
    """
    Structure of the data stored in the pickle database.
    """

    member_data = mm.fields.Nested(
        UserEventsFileSchema,
        # Some zips didn't have the member we wanted.
        load_default = None,
        metadata = {
            'description': 'JSON data from the matching member file.',
        },
    )

    path = mm.fields.String(
        required = True,
        metadata = {
            'description': 'Path to ZIP.',
        },
    )

    path_data = mm.fields.Dict(
        required = True,
        metadata = {
            'description': 'Data parsed from the path.',
        },
    )
