import marshmallow as mm

from crew_brief import constants
from crew_brief import type_convert

from .field import DataStringField
from .field import IntOrStringField

class UserEventSchema(mm.Schema):
    """
    Single item from userEvents list.
    """

    eventTimeStamp = mm.fields.DateTime(
        format = constants.ZDATETIME_FORMAT,
        required = True,
    )

    eventType = mm.fields.String(
        missing = None,
    )

    status = mm.fields.String(
        missing = None,
    )

    eventDetails = mm.fields.Dict(
        # Dict for missing key.
        missing = dict,
    )

    @mm.post_load
    def post_load(self, data, **kwargs):
        """
        Recursively update string values for detected types.
        """
        event_details = data['eventDetails']
        type_convert.rtype_update(event_details)
        return data


class UserEventsSchema(mm.Schema):
    """
    Data from the JSON file UserEvents.txt
    """

    legIdentifier = DataStringField(
        part_names = constants.LEG_IDENTIFIER_PARTS,
        sep = '.',
        part_types = dict(
            date = type_convert.DateConverter(
                constants.LEG_IDENTIFIER_DATE_FORMAT
            ),
        ),
        required = True,
        metadata = dict(
            description =
                'legIdentifier is a string with values packed into it.',
        ),
    )

    userId = IntOrStringField(
        metadata = dict(
            description =
                'userId is usually an integer but sometimes a'
                ' username string.',
        ),
    )

    userEvents = mm.fields.Nested(
        UserEventSchema,
        many = True,
        required = True,
        metadata = dict(
            description =
                'If present, userEvents is a list of many different dicts.',
        ),
    )


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
