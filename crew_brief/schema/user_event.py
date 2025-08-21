import marshmallow as mm

from crew_brief import constants
from crew_brief import convert
from crew_brief.model.user_event import UserEvent
from crew_brief.model.user_event import UserEventsFile

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
        load_default = None,
    )

    status = mm.fields.String(
        load_default = None,
    )

    eventDetails = mm.fields.Dict(
        # Dict for missing key.
        load_default = dict,
    )

    @mm.post_load
    def post_load(self, data, **kwargs):
        """
        Recursively update string values for detected types in eventDetails;
        and return an instance of the model.
        """
        event_details = data['eventDetails']
        convert.deep_convert(event_details)
        instance = UserEvent(**data)
        return instance


class UserEventsFileSchema(mm.Schema):
    """
    Data from the JSON file UserEvents.txt
    """

    legIdentifier = DataStringField(
        part_names = constants.LEG_IDENTIFIER_PARTS,
        sep = '.',
        part_types = dict(
            date = convert.DateConverter(
                constants.SHORT_DATE_FORMAT
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

    @mm.post_load
    def post_load(self, data, **kwargs):
        instance = UserEventsFile(**data)
        return instance
