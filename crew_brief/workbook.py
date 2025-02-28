import copy

from itertools import tee

from crew_brief import output
from crew_brief import rowifier
from crew_brief import shapers

def select_event_details_row(user_event_row):
    return (
        # Has original data.
        user_event_row.original
        and
        # And it's a user event header row. Though it should not matter between
        # header and values rows.
        'user_event_fields_and_values' in user_event_row.style_hint
        and
        'header' in user_event_row.style_hint
    )

def max_event_details_length(styled_rows):
    iterable = (
        len(user_event_row) for user_event_row in styled_rows
        if select_event_details_row(user_event_row)
    )
    return max(iterable, default=0)

def right_align_original(styled_rows, max_len):
    """
    Generate padded out styled_rows objects to have the original data appear in
    the rightmost position.
    """
    user_event_rows = []
    max_len = 0

    # Need two iterators to go through twice.
    rows1, rows2 = tee(styled_rows)

    # Find the max length.
    max_len = max_event_details_length(rows1)

    # Pad selected row and yield the others as-is.
    for user_event_row in rows2:
        if select_event_details_row(user_event_row):
            # Pad and flatten original into the row.
            pad = (None, ) * (max_len - len(user_event_row.row))
            user_event_row.row = user_event_row.row + pad + (user_event_row.original, )
        yield user_event_row

def build_workbook(zip_data, typed_zip_data):
    # Raise for member_data is None
    untyped_member_data = zip_data['member_data']
    if untyped_member_data is None:
        raise ValueError('member_data is None.')

    # Copy and apply custom data shaping.
    typed_member_data = typed_zip_data['member_data']
    shaped_member_data = copy.deepcopy(typed_member_data)
    member_data_shaper = shapers.MemberDataShaper()
    member_data_shaper(shaped_member_data)

    # Turn data into rows.
    user_events_rowifier = rowifier.UserEventsRowifier()
    rows = user_events_rowifier(shaped_member_data, untyped_member_data)

    # Push last cell of row to the right.

    # Need two iterators to go through twice.
    rows1, rows2 = tee(rows)
    max_len = max_event_details_length(rows1)
    rows = right_align_original(rows2, max_len)

    # Create workbook.
    excel_converter = output.ExcelConverter()
    wb = excel_converter(
        rows,
        event_details_length=max_len - 3,
        hide_event_details = True,
    )

    return wb

def build_workbook_for_member(untyped_member_data, typed_member_data):
    # Copy and apply custom data shaping.
    shaped_member_data = copy.deepcopy(typed_member_data)
    member_data_shaper = shapers.MemberDataShaper()
    member_data_shaper(shaped_member_data)

    # Turn data into rows.
    user_events_rowifier = rowifier.UserEventsRowifier()
    rows = user_events_rowifier(shaped_member_data, untyped_member_data)

    # Push last cell of row to the right.

    # Need two iterators to go through twice.
    rows1, rows2 = tee(rows)
    max_len = max_event_details_length(rows1)
    rows = right_align_original(rows2, max_len)

    # Create workbook.
    excel_converter = output.ExcelConverter()
    wb = excel_converter(
        rows,
        event_details_length=max_len - 3,
        hide_event_details = True,
    )

    return wb
