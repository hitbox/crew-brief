import json

from crew_brief.sorting import is_container
from crew_brief.sorting import pad_list
from crew_brief.sorting import split_dict

class RowSplit:
    """
    Split user events and original data into multiple dict-tables fit for
    producing single row rows.
    """

    def __init__(self, main_keys, right_side_keys, case_sensitive=True):
        self.main_keys = main_keys
        self.right_side_keys = right_side_keys
        self.case_sensitive = case_sensitive

    def __call__(self, user_events1, original_data):
        # Split the rows of dicts into two lists or rows. One for the unnested
        # main data and one for the nested event details dicts.
        splits = (split_dict(row, self.main_keys, self.case_sensitive) for row in user_events1)
        main_rows, details_rows = zip(*splits)

        # Update dicts for special structures.
        #details_rows = [user_event.to_excel() for user_event in details_rows]
        #update_dicts(details_rows)

        # Split middle and right sides.
        gen = (
            split_dict(row['eventDetails'], self.right_side_keys, self.case_sensitive)
            for row in details_rows
        )
        right_rows, middle_rows_before = zip(*gen)

        # Lists of values for main data.
        main_rows = [[data[key] for key in self.main_keys] for data in main_rows]
        main_rows = [row + [None] * (3 - len(row)) for row in main_rows]

        # Expand into rows of alternating keys and values.
        middle_rows = [
            [item for pair in middle_data.items() for item in pair]
            for middle_data in middle_rows_before
        ]

        # NOTES:
        # - min_length is used because the headers will always be there and the
        #   data rows need to match, especially when empty.
        middle_rows = pad_list(middle_rows, min_length=2)

        right_rows = [list(data.values()) for data in right_rows]
        right_rows = pad_list(right_rows, min_length=1)

        # Single column for original data.
        original_details_rows = [
            [json_string(data_row)] for data_row in original_data['userEvents']
        ]

        return (main_rows, middle_rows, right_rows, original_details_rows)


def update_dicts(details_rows):
    # TODO
    # - Remove this in favor of something just before cells are written to the
    #   worksheet.
    for detail in details_rows:
        for key, val in detail['eventDetails'].items():
            if isinstance(val, dict) and 'name' in val and 'rank' in val:
                detail['eventDetails'][key] = f'{val["rank"]} {val["name"]}'

def json_string(data):
    order = [
        'eventTimeStamp',
        'status',
        'eventType',
        'eventDetails',
    ]

    def sort_key(key):
        if key in order:
            return (0, order.index(key))
        else:
            return (1, key)

    keys = sorted(data, key=sort_key)
    return json.dumps({k: data[k] for k in keys})

def keys_gt(data, *keys, value=0):
    """
    All keys exist in data and their values are greater than `value`.
    """
    return all(key in data and data[key] > value for key in keys)

def is_reasonable(val):
    """
    Key-value pairs have reasonable data. Intended to filter out useless info.
    """
    return keys_gt(val, 'minutes', 'fuel')

def format_dict(data):
    result = {}
    for key, val in data.items():
        if is_container(val):
            if val:
                # Populated container
                if not is_reasonable(val):
                    continue
                # Include populated container
                result[key] = val
        else:
            result[key] = val
    return result
