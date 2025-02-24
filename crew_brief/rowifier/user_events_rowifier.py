from crew_brief import constants
from crew_brief.sorting import EventDetailsKey
from crew_brief.unfold import unfold_dict

class UserEventRow:
    def __init__(self, style_hint, row, original, keys):
        self.style_hint = style_hint
        self.row = row
        self.original = original
        self.keys = keys

    def __len__(self):
        return len(self.row)

    def __iter__(self):
        yield self.style_hint
        yield self.row
        yield self.original


class UserEventRowifier:
    """
    Yield a userEvent dict as a row with eventDetails, if present, as a nested
    table to the right.
    """

    header = [
        'eventTimeStamp',
        'status',
        'eventType',
        'eventDetails',
    ]
    first_three = header[:3]

    def __init__(self, event_details_rowifier=None):
        self.event_details_rowifier = event_details_rowifier or unfold_dict
        self.sorting = EventDetailsKey()

    def __call__(self, user_events1, user_events2):
        """
        Create row for a single userEvent item in the list.
        """
        first_fields_and_values = self.get_first_fields(user_events1)
        event_details1, event_details2 = self.get_event_details(user_events1, user_events2)

        if not self.event_details_are_consistent(event_details1, event_details2):
            raise ValueError('eventDetails truthiness differ.')

        subheader, subvalues = self.process_event_details(event_details1, event_details2)

        if subheader and subvalues:
            rows = self.create_user_event_rows(
                first_fields_and_values,
                subheader,
                subvalues,
                user_events1,
                user_events2,
            )
            yield from rows
        else:
            yield self.create_single_row(first_fields_and_values)

    def get_first_fields(self, user_events):
        """
        Extract the first three fields from user_events.
        """
        return tuple(user_events.get(key) for key in self.first_three)

    def get_event_details(self, user_events1, user_events2):
        """
        Retrieve eventDetails from both user event dictionaries.
        """
        return user_events1.get('eventDetails'), user_events2.get('eventDetails')

    def event_details_are_consistent(self, event_details1, event_details2):
        """
        Check if the truthiness of eventDetails is the same for both events.
        """
        return bool(event_details1) == bool(event_details2)

    def process_event_details(self, event_details1, event_details2):
        """
        Process event details to generate subheader and subvalues.
        """
        if event_details1 and event_details2:
            subheader, subvalues = self.event_details_rowifier(
                event_details1,
                sep = constants.NESTED_KEY_SEP,
            )
            return self.filter_empty_items(subheader, subvalues)
        return None, None

    def filter_empty_items(self, subheader, subvalues):
        """
        Filter out pairs where the value is an empty container.
        """
        items = zip(subheader, subvalues)
        items = [(key, val) for key, val in items if val not in ('', [], {}, set())]

        if items:
            # Unzip into subheader and subvalues
            return zip(*items)
        return (None, None)

    def create_user_event_rows(
        self,
        first_fields_and_values,
        subheader,
        subvalues,
        user_events1,
        user_events2,
    ):
        """
        Create user event rows with subheader and subvalues.
        """
        event_type = user_events1['eventType']
        sort_key = lambda item: self.sorting(item[0], event_type)
        items = sorted(zip(subheader, subvalues), key=sort_key)
        subheader, subvalues = zip(*items)

        # Main userEvent values plus header for eventDetails.
        row = first_fields_and_values + subheader
        keys = tuple(self.first_three) + subheader

        yield UserEventRow(
            style_hint = 'user_event_fields_and_values header',
            row = row,
            original = user_events2.get('eventDetails'),
            keys = keys,
        )

        # Right-aligned values for eventDetails.
        row = (None,) * len(first_fields_and_values) + tuple(val for _, val in items)
        yield UserEventRow(
            style_hint = 'user_event_fields_and_values subrow',
            row = row,
            original = None,
            keys = keys,
        )

    def create_single_row(self, first_fields_and_values):
        """
        Create a single row when no subdata is available.
        """
        return UserEventRow(
            style_hint='user_event_fields_and_values singlerow',
            row=first_fields_and_values,
            original=None,
            keys=self.first_three,
        )


class UserEventsRowifier:
    header = [
        'eventTimeStamp',
        'status',
        'eventType',
        'eventDetails',
    ]

    def __init__(self, user_event_rowifier=None, leg_identifier_labels=None):
        self.user_event_rowifier = user_event_rowifier or UserEventRowifier()
        self.leg_identifier_labels = leg_identifier_labels or constants.LEG_IDENTIFIER_LABELS

    def styled_empty_row(self):
        """
        Return an empty styled row.
        """
        return UserEventRow(
            style_hint = 'empty',
            row = tuple(),
            original = None,
            keys = None,
        )

    def extra_information(self, member_data):
        """
        Generate extra information at the end, including legIdentifier and
        userId.
        """
        yield self.styled_empty_row()
        yield UserEventRow(
            style_hint='legIdentifier super-header',
            row=('legIdentifier',),
            original=None,
            keys=('legIdentifier',) * 2,
        )

        label_getter = self.leg_identifier_labels.__getitem__
        for key in self.leg_identifier_labels:
            value = member_data['legIdentifier'][key]
            label = label_getter(key)
            yield UserEventRow(
                style_hint='legIdentifier field_and_value',
                row=(label, value),
                original=None,
                keys=(key, key),
            )

        yield self.styled_empty_row()
        yield UserEventRow(
            style_hint='userId field_and_value',
            row=('userId', member_data['userId']),
            original=None,
            keys=('userId', 'userId'),
        )

    def event_lists_are_consistent(self, user_events1, user_events2):
        """
        Check if the truthiness of userEvents is the same for both lists.
        """
        return bool(user_events1) == bool(user_events2)

    def __call__(self, member_data, original_data):
        """
        Generate user events rows from the member data and original data.
        """
        user_events1 = member_data.get('userEvents')
        user_events2 = original_data.get('userEvents')

        if not self.event_lists_are_consistent(user_events1, user_events2):
            raise ValueError('userEvents truthiness differ.')

        if user_events1 and user_events2:
            event_pairs = zip(user_events1, user_events2, strict=True)
            for user_event1, user_event2 in event_pairs:
                yield from self.user_event_rowifier(user_event1, user_event2)

        yield from self.extra_information(member_data)
