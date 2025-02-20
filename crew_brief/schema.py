import datetime

import marshmallow as mm

from . import constants
from . import type_convert

def leg_identifier_date(string):
    return datetime.datetime.strptime(string, "%d%b%Y").date()

class DataStringField(mm.fields.Field):
    """
    Split string into dict.
    """

    def __init__(self, part_names, sep, part_types=None, **kwargs):
        """
        :param part_names:
            Ordered list of names for the parts of the string.
        :param sep:
            Separator.
        :param part_types:
            Dict of names to functions to apply to resulting split-dict.
        :param kwargs:
            Remaining keyword arguments to pass to parent field class.
        """
        self.part_names = part_names
        self.sep = sep
        self.part_types = part_types
        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        value_data = dict(zip(self.part_names, value.split(self.sep)))
        if self.part_types:
            for key, func in self.part_types.items():
                key_value = value_data[key]
                value_data[key] = func(key_value)
        return value_data


class IntOrStringField(mm.fields.Field):
    """
    Try make integer falling back to string.
    """

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, int):
            return value

        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return value

        raise mm.ValidationError("Invalid type: Must be a string or integer.")


class UserEventSchema(mm.Schema):
    """
    Single item from userEvents.
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
        # Recursively update string values for detected types.
        event_details = data['eventDetails']
        type_convert.rtype_update(event_details)
        return data


class MemberSchema(mm.Schema):
    """
    Data from the JSON file UserEvents.txt
    """

    # legIdentifier is a string with values packed into it.
    legIdentifier = DataStringField(
        part_names = constants.LEG_IDENTIFIER_PARTS,
        sep = '.',
        part_types = dict(
            date = leg_identifier_date,
        ),
        required = True,
    )

    # userId is usually an integer but sometimes a username string.
    userId = IntOrStringField()

    # if present, userEvents is a list of many different dicts.
    userEvents = mm.fields.Nested(
        UserEventSchema,
        many = True,
        required = True,
    )


class PickleSchema(mm.Schema):
    """
    Structure of the data stored in the pickle database.
    """

    member_data = mm.fields.Nested(
        MemberSchema,
        # Some zips didn't have the member we wanted.
        missing = None,
    )

    path = mm.fields.String(
        required = True,
    )

    path_data = mm.fields.Dict(
        required = True,
    )


pickle_schema = PickleSchema()
