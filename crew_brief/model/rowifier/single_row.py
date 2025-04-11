from crew_brief.sorting import pad_list
from crew_brief.sorting import split_dict

from .mixin import ConsistencyMixin
from .user_event_row import UserEventRow

class SingleRowifier(ConsistencyMixin):
    """
    Produce key-value rows for output.
    """

    def __init__(self, right_side_keys):
        self.right_side_keys = right_side_keys

    def __call__(self, member_data, original_data):
        # List of dicts with optional eventDetails dicts inside.
        user_events1 = member_data.get('userEvents')
        user_events2 = original_data.get('userEvents')

        if not self.event_lists_are_consistent(user_events1, user_events2):
            raise ValueError('userEvents truthiness differ.')

        mains = []
        lefts = []
        rights = []
        for user_event in user_events1:
            event_details, main_dict = split_dict(user_event, ['eventDetails'])
            mains.append(main_dict)
            right_dict, left_dict = split_dict(
                event_details['eventDetails'],
                self.right_side_keys
            )
            lefts.append(left_dict)
            rights.append(right_dict)

        max_left_row_len = max(len(data) for data in lefts)

        details = []
        for main, left, right in zip(mains, lefts, rights, strict=True):
            # Add main row.
            row = list(main.values())
            # Add lefts as flattened keys and values.
            row += [thing for item in left.items() for thing in item]
            if right:
                # Padding for right row.
                row += [None for _ in range(max_left_row_len - len(row)) for _ in range(2)]

            row += [thing for item in right.items() for thing in item]
            details.append(row)

        yield from details
        return

        max_detail_row_len = max(len(data) for data in details)

        # TODO
        # - right side rows are not going fully to the right.
        # - original_data doesn't seem to be what we need to append it to the
        #   rows.
        # - Need to add the original data for each row in hidden column.
        # - Need key sorting from original too.
        # - Header row.
        # - Extra data at the bottom.

        for detail, original in zip(details, original_data):
            # Padding for original
            detail += [None for _ in range(max_detail_row_len - len(detail))]
            yield detail + [original]


def key_then_value(rows):
    for key, value in rows:
        yield key
        yield value
