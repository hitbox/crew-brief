from operator import itemgetter

from . import constants
from . import nodes
from . import sorting

containers = (dict, list, set, tuple)

class StyledData:

    def __init__(self, value, style):
        # style: dict of attribute names to value to stick on that row.
        self.value = value
        self.style = style


class SingleRowIterator:
    # XXX
    # This is the original data-to-row iterator.

    def __call__(self, user_events_data):
        # TODO
        # - Dedicated row iterator class for this.
        # Intended to just output the raw values
        yield self.header
        for user_event in data['userEvents']:
            row = self.get_first_three(user_event)
            if event_details := user_event.get('eventDetails'):
                items = nodes.visit_for_dict(
                    event_details,
                    key_sort = self.important_keys,
                )
                for parents, value in items:
                    row += parents + (value, )
            yield row


class EventDetailsIterator:
    # Sub-table row iterator for the eventDetails dict.
    pass


class DoubledRowIterator:
    """
    Output data from UserEvents.txt JSON as rows where the eventDetails is
    structured as a subtable on the right.
    """

    header = ['eventTimeStamp', 'status', 'eventType', 'eventDetails']
    first_three = header[:3]
    get_first_three = itemgetter(*first_three)

    def __init__(self, include_original=True):
        self.include_original = include_original
        self.important_keys = sorting.EventDetailsKey()

    def is_simple_single_dict(self, data):
        if len(data) == 1:
            value = next(iter(data.values()))
            if not isinstance(value, (dict, list, set, tuple)):
                return True

    def iter_header_available(self, user_event, original_user_event):
        return iter(user_event[key] for key in self.header if key in user_event)

    def has_full_header(self, user_event):
        return all(key in user_event for key in self.first_three)

    def row_with_event_details(self, row, user_event, event_details, original_data):
        if self.is_simple_single_dict(event_details):
            # Key-value, single row for single item dict.
            key, val = next(iter(event_details.items()))
            rv = row + (key, val)
        else:
            # Row of keys-header and then an indented row for values.
            keys = []
            values = []
            empty_first = (None,) * len(row)
            details_iter = nodes.visit_for_dict(
                event_details,
                key_sort = self.important_keys,
            )
            for parents, value in details_iter:
                if len(set(parents)) == 1:
                    # Collapse parent keys that are all the same.
                    keys.append(parents[0])
                else:
                    keys.append(' '.join(parents))
                values.append(value)
            # TODO: find the rightmost and pad and include event_details

            # Yield field names.
            yield row + tuple(keys)

            rv = (None,)*len(row) + tuple(values)

        if self.include_original:
            rv += original_data
        yield rv

    def row_with_first_three(self, shaped_user_event, original_user_event):
        row = self.get_first_three(shaped_user_event)
        shaped_event_details = shaped_user_event.get('eventDetails')
        if not shaped_event_details:
            yield row
        else:
            # TODO
            # - Collapse rows whose only difference is the time because
            #   they're hammering some button. Keep the last.
            original_event_details = original_user_event.get('eventDetails')
            original_data = tuple(map(str, (original_event_details, shaped_event_details)))
            if isinstance(shaped_event_details, dict):
                rows_iter = self.row_with_event_details(
                    row,
                    shaped_user_event,
                    shaped_event_details,
                    original_data,
                )
                yield from rows_iter
            else:
                rv = row + (shaped_event_details, )
                if self.include_original:
                    rv += original_data
                return rv

    def row(self, typed_user_event, user_event):
        if self.has_full_header(typed_user_event):
            # Full row, probably has eventDetails
            yield from self.row_with_first_three(typed_user_event, user_event)
        else:
            # Take whatever is available in header order.
            row = tuple(self.iter_header_available(typed_user_event, user_event))
            yield row

    def __call__(self, typed_user_events, original_user_events):
        pairs = zip(typed_user_events, original_user_events)
        for typed_user_event, original_user_event in pairs:
            row = self.row(typed_user_event, original_user_event)
            row = [string_container(value) for value in row]
            yield row

    def __call__(self, typed_user_events, original_user_events):
        for typed_user_event in original_user_events:
            # TODO
            # - yield header here or in excel?
            # - yield values for header

            row = [typed_user_event.get(key) for key in self.header]

            for index, value in enumerate(row):
                row[index] = string_container(value)

            yield row


class EventDetailsRowifier:

    def __call__(self, event_details):
        row = []
        # TODO
        # - Sort important keys.
        for key, value in event_details.items():
            row.append(key)
            row.append(value)
        yield tuple(row)


class UserEventRowifier:

    header = ['eventTimeStamp', 'status', 'eventType', 'eventDetails']
    first_three = header[:3]
    get_first_three = itemgetter(*first_three)

    default_event_details_rowifier_class = EventDetailsRowifier

    def __init__(self, event_details_rowifier=None):
        if event_details_rowifier is None:
            event_details_rowifier = self.default_event_details_rowifier_class()
        self.event_details_rowifier = event_details_rowifier

    def __call__(self, member_data, original=None):
        # TODO
        # - Expand eventDetails
        # - Return what type of row we're returning, "header" or "values"

        first_fields_and_values = tuple(member_data.get(key) for key in self.first_three)

        event_details = member_data.get('eventDetails')
        if event_details:
            for event_details_row in self.event_details_rowifier(event_details):
                row = first_fields_and_values + event_details_row
                if original is not None:
                    row += (str(original['eventDetails']), )
                row = ('user_event_fields_and_values', row)
                yield row
        else:
            row = first_fields_and_values
            row = ('user_event_fields_and_values', row)
            yield row


class MemberDataRowifier:

    header = [
        'eventTimeStamp',
        'status',
        'eventType',
        'eventDetails',
    ]

    def __init__(
        self,
        user_event_rowifier = None,
        leg_identifier_keys = None,
        leg_identifier_labels = None
    ):
        if user_event_rowifier is None:
            user_event_rowifier = UserEventRowifier()
        self.user_event_rowifier = user_event_rowifier

        if leg_identifier_keys is None:
            leg_identifier_keys = constants.LEG_IDENTIFIER_PARTS
        self.leg_identifier_keys = leg_identifier_keys

        if leg_identifier_labels is None:
            leg_identifier_labels = constants.LEG_IDENTIFIER_LABELS
        self.leg_identifier_labels = leg_identifier_labels

    def row_values_for_excel(self, row):
        # Finalize values for Excel
        # TODO
        # - lists
        # - expand dicts to doubled rows
        type_ = type(row)

        def str_leave_none(value):
            if value is None:
                return value
            return str(value)

        return type_(map(str_leave_none, row))

    def styled_empty_row(self):
        return ('empty', tuple())

    def __call__(self, member_data, original=None):
        # XXX
        # - Consider using dicts to avoid having to know what order the values
        #   are coming back as.

        # Yield header row.
        yield ('header', tuple(self.header))

        # User events rows.
        user_events = member_data.get('userEvents')
        if user_events:
            if original is not None:
                original_user_events = original['userEvents']
            else:
                original_user_events = None
            for user_event, original_user_event in zip(user_events, original_user_events):
                pairs = self.user_event_rowifier(
                    user_event,
                    original = original_user_event,
                )
                for row_type, row in pairs:
                    row = self.row_values_for_excel(row)
                    yield (row_type, row)

        # Extra information at the end.

        # Field names for legIdentifier.
        yield self.styled_empty_row()
        row = ('legIdentifier', )
        yield ('header', row)

        label_getter = self.leg_identifier_labels.__getitem__
        row = tuple(map(label_getter, self.leg_identifier_keys))
        row = self.row_values_for_excel(row)
        yield ('legIdentifier header', row)

        # Values for legIdentifier.
        value_getter = member_data['legIdentifier'].__getitem__
        row = tuple(map(value_getter, self.leg_identifier_keys))
        row = self.row_values_for_excel(row)
        yield ('legIdentifier values', row)

        # userId field name and value row.
        yield self.styled_empty_row()
        for key in ['userId']:
            row = (key, member_data[key])
            row = self.row_values_for_excel(row)
            yield ('userId field_and_value', row)


def is_container(value):
    return isinstance(value, containers)

def string_container(value):
    if is_container(value):
        value = str(value)
    return value
