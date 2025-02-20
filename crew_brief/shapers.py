import copy

from . import collapse
from . import constants
from . import type_convert

class EventDetailsShaper:
    """
    Rearrange the data from items in the eventDetails dict.
    """

    # Specially handled structures identified by key.
    keys_as_values = set([
        'assignedLandingDuty',
        'assignedTakeOffDuty',
        'withdrawnLandingDuty',
        'withdrawnTakeOffDuty',
    ])

    # TODO
    # - Put this on the sheet as a nested little table.
    fuel_keys = set([
        'Discretionary Fuel',
        'Extra Fuel',
        'Taxi Fuel',
    ])

    value_only_event_type = set([
        'CreateRoom',
        'FlaggedNOTAM',
        'ResetRoute',
    ])

    def __init__(self):
        self.convert_data_type = type_convert.TypeConverter(
            # Important order, especially for int and float.
            type_convert.DateTimeConverter(
                constants.ZDATETIME_FORMAT,
            ),
            type_convert.FloatConverter(),
            type_convert.IntegerConverter(),
        )
        self.collapse_versioned = collapse.EventTypeVersionedCollapse(
            # eventType key to tuple pairs of new-to-old keys from eventDetails.
            event_type_mapping = dict(
                ReceivedAcceptedBP = [
                    ('latestBpSequenceNumber', 'oldBpSequenceNumber'),
                    ('latestBpVersion', 'oldBpVersion'),
                ],
                ReceivedDeclinedBP = [
                    ('receivedBpSequenceNumber', 'existingBpSequenceNumber'),
                    ('receivedBpVersion', 'existingBpVersion'),
                ],
            ),
        )
        self.collapse_key_data = collapse.DataKeyCollapse(
            'assignedLandingDuty',
            'assignedTakeOffDuty',
            'withdrawnLandingDuty',
            'withdrawnTakeOffDuty',
        )

    def convert_user_events(self, event_details):
        """
        Reshape, condense and convert types for userEvent items.

        :param event_details: eventDetails data.
        """
        if isinstance(event_details, dict):
            for key, value in event_details.items():
                if key in self.keys_as_values:
                    # Join key-data and values and replace weird sub-dict.
                    event_details[key] = self.collapse_key_data(value)
                if isinstance(value, str):
                    typed = self.convert_data_type(value)
                    if typed:
                        event_details[key] = typed
                else:
                    self.convert_user_events(value)

    def convert(self, member_data):
        # TODO
        # - Collapse runs of duplicate eventDetails.
        # - Save shaping activity to log onto the output.
        member_data = copy.deepcopy(member_data)
        for user_event in member_data['userEvents']:
            if event_details := user_event.get('eventDetails'):
                if event_type := user_event.get('eventType'):
                    if event_type in self.value_only_event_type:
                        # Remove one item sub-dict and keep first value.
                        assert len(event_details) == 1
                        value = next(iter(event_details.values()))
                        user_event['eventDetails'] = value
                    # Collapse versions without a difference.
                    self.collapse_versioned(event_type, event_details)
                self.convert_user_events(event_details)
        return member_data

    def convert_many(self, member_data_iterable):
        for member_data in member_data_iterable:
            yield self.convert(member_data)


class EventDetailsShaper:

    expand_key_as_value = set([
        'assignedLandingDuty',
        'assignedTakeOffDuty',
        'withdrawnLandingDuty',
        'withdrawnTakeOffDuty',
    ])

    def expand_item(self, data):
        assert isinstance(data, dict)
        assert len(data) == 1
        the_item = next(iter(data.items()))
        return dict(zip(['rank', 'name'], the_item))

    def __call__(self, event_details):
        for key, val in event_details.items():
            if key in self.expand_key_as_value:
                # val is a dict, expand its keys that should have been values.
                event_details[key] = self.expand_item(val)


class UserEventShaper:

    default_event_details_shaper_class = EventDetailsShaper

    def __init__(self, event_details_shaper=None):
        if event_details_shaper is None:
            event_details_shaper = self.default_event_details_shaper_class()
        self.event_details_shaper = event_details_shaper

    def __call__(self, user_event):
        if 'eventDetails' in user_event:
            self.event_details_shaper(user_event['eventDetails'])


class MemberDataShaper:

    default_user_event_shaper_class = UserEventShaper

    def __init__(self, user_event_shaper=None):
        if user_event_shaper is None:
            user_event_shaper = self.default_user_event_shaper_class()
        self.user_event_shaper = user_event_shaper

    def __call__(self, member_data):
        for user_event in member_data['userEvents']:
            self.user_event_shaper(user_event)
