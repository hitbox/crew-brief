from .constants import NESTED_KEY_SEP

class EventDetailsKey:
    """
    Callable ordering for eventDetails' keys. Mostly for sorting important keys
    to the front.
    """

    # Ordering list.
    # Empty lines to indicate keys that usually only appear together.
    # Consider eventDetails ordering by eventType.
    detail_keys = [

        # Many different eventType values.
        'waypoint',

        # eventType == DirectTo
        'fromWaypoint',
        'toWaypoint',
    ]

    event_type_ordering = dict(
        ReceivedAcceptedBP = [
            'receivedFromDevice',
            'categoriesReceived',
            'latestBpSequenceNumber',
            'latestBpVersion',
            'oldBpSequenceNumber',
            'oldBpVersion',
        ],
        SharedBP = [
            'sharedWithDevice',
            'categoriesShared',
        ],
        DutyAssignment = [
            NESTED_KEY_SEP.join(['assignedTakeOffDuty', 'name']),
            NESTED_KEY_SEP.join(['assignedTakeOffDuty', 'rank']),

            NESTED_KEY_SEP.join(['assignedLandingDuty', 'name']),
            NESTED_KEY_SEP.join(['assignedLandingDuty', 'rank']),

            NESTED_KEY_SEP.join(['withdrawnTakeOffDuty', 'name']),
            NESTED_KEY_SEP.join(['withdrawnTakeOffDuty', 'rank']),
        ],
    )

    def __call__(self, key, event_type):
        """
        If key is present in our ordering list return the index. Otherwise
        return the length of the list so as to sort the rest with the same
        precedence.
        """
        # Sorting is off. The subheader is somehow coming out different than
        # the values.
        # Also this one need to offset the event_type_ordering by the len(detail_keys)

        # Try to find an ordering list by eventType and then detail_keys.
        ordering_list = None
        if event_type in self.event_type_ordering:
            ordering_list = self.event_type_ordering[event_type]
        elif key in self.detail_keys:
            ordering_list = self.detail_keys

        # Use the ordering list or make the sort key all the same priority but
        # after any detail_keys.
        if ordering_list and key in ordering_list:
            return ordering_list.index(key)
        else:
            return len(self.detail_keys)


def padded_keys(
    data,
    sort_key = None,
    reverse = False,
    pad_value = None,
    only = None,
):
    """
    Columnize the data. Generate rows of sorted keys padded to align them in
    each row.
    """
    unique_keys = {key for row in data for key in row}
    sorted_keys = sorted(unique_keys, key=sort_key, reverse=reverse)

    def value(row, key):
        if key in row:
            return key
        elif not only or key in only:
            return pad_value

    for row in data:
        yield [value(row, key) for key in sorted_keys]

def tailed(data, tailkeys, pad_value=None):
    main_keys = [key for row in data for key in row if key not in tailkeys]
    main_width = len(main_keys)

    for row in data:
        left = [row.get(k) for k in main_keys if k in row]
        pad_len = main_width - len(left)
        # collapse missing keys left
        padded_left = left + [pad_value] * pad_len
        tail = [row.get(k, pad_value) for k in tailkeys]
        yield padded_left + tail

def for_keys(data, keys):
    for row in data:
        yield {key: val for key, val in row.items() if key in keys}

def split_dict(data, keys):
    extracted = {k: data[k] for k in keys if k in data}
    remaining = {k: v for k, v in data.items() if k not in keys}
    return (extracted, remaining)

def pad_list(list_, pad_value=None):
    max_length = max(map(len, list_))

    # Allow different row types or enforce all the same?
    # For now, we allow different.

    def padding(row):
        if isinstance(row, list):
            pad = [pad_value]
        elif isinstance(row, tuple):
            pad = (pad_value,)
        else:
            raise ValueError(f'Invalid row type {type(row)}.')
        return pad

    return [row + padding(row) * (max_length - len(row)) for row in list_]
