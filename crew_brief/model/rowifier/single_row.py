from crew_brief.sorting import expand_dict
from crew_brief.sorting import pad_list
from crew_brief.sorting import split_dict

from .common import HEADER
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

        def filter_dict(dict_):
            def f(k, v):
                if isinstance(v, (dict, list, tuple)):
                    if v:
                        return v
                else:
                    return v
            return {k: v for k, v in dict_.items() if f(k, v)}

        def format_dict(dict_):
            for key, val in dict_.items():
                if isinstance(val, dict):
                    # Format dict value for rank and name.
                    if 'rank' in val and 'name' in val:
                        dict_[key] = val['rank'] + ' ' + val['name']
            return dict_

        # Split the user events into three parts.
        mains = []
        middle = []
        rights = []
        for user_event in user_events1:
            event_details, main_dict = split_dict(user_event, ['eventDetails'])
            mains.append(list(main_dict.values()))
            right_dict, middle_dict = split_dict(
                event_details['eventDetails'],
                self.right_side_keys
            )
            middle.append(expand_dict(format_dict(filter_dict(middle_dict))))
            rights.append(expand_dict(format_dict(filter_dict(right_dict))))

        # Pad middle and right tables.
        middle = pad_list(middle)
        rights = pad_list(rights)

        yield HEADER
        items = zip(mains, middle, rights, user_events2, strict=True)
        for row, middle, right, original in items:
            yield row + middle + right + [original]

        return

        max_detail_row_len = max(len(data) for data in details)

        # TODO
        # - Need key sorting from original too.
        # - Add "original data" field name aligned properly.
        # - Extra data at the bottom.

        for detail, original in zip(details, original_data):
            # Padding for original
            detail += [None for _ in range(max_detail_row_len - len(detail))]
            yield detail + [original]


def key_then_value(rows):
    for key, value in rows:
        yield key
        yield value
