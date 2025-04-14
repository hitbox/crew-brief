import openpyxl

from crew_brief.output.excel import ExcelConverter
from crew_brief.sorting import join_tables
from crew_brief.sorting import max_cols

from .excel_row import ExcelRow
from .mixin import ConsistencyMixin
from .style import KeyStyle
from .style import StatusStyle
from .style import ValueStyle

header_style = ExcelConverter.styles['header_style']
full_datetime_style = ExcelConverter.styles['full_datetime_style']

class SingleRowifier(ConsistencyMixin):
    """
    Produce key-value rows for output.
    """

    def __init__(self, row_splitter):
        self.row_splitter = row_splitter

    def __call__(self, member_data, original_data):
        """
        Convert typed and original JSON UserEvent data into rows for Excel.
        """
        # Convert to Excel
        member_data = member_data.__excel__()

        # List of dicts with optional eventDetails dicts inside.
        user_events1 = member_data.get('userEvents')
        user_events2 = original_data.get('userEvents')

        if not self.event_lists_are_consistent(user_events1, user_events2):
            raise ValueError('userEvents truthiness differ.')

        items = self.row_splitter(user_events1, original_data)
        main_rows, middle_rows, right_rows, original_details_rows = items

        # Headers
        max_middle_cols = max_cols(middle_rows)
        middle_header = ['eventDetails', None] + ([None] * (max_middle_cols - 2))
        right_header = self.row_splitter.right_side_keys
        original_header = ['Original']

        header = self.row_splitter.main_keys + middle_header + right_header + original_header

        # Header Styling
        header_styles = (
            # Main keys header
            [header_style] * len(self.row_splitter.main_keys)
            # Middle, eventDetails header with merge for max row
            + [header_style] + [None] * (len(middle_header) - 1)
            # Right side of eventDetails
            + [header_style] * len(self.row_splitter.right_side_keys)
            # Original
            + [header_style]
        )

        excel_header_row = ExcelRow(
            header,
            styles = header_styles,
        )

        # Suspect check is necessary for when there's only one or none
        # eventDetails.
        end_column = 4 + (max_middle_cols - 1)
        if end_column > 4:
            excel_header_row.merge = (4, end_column)
        yield excel_header_row

        # Yield formatted data rows.
        assert all(len(row) == 3 for row in main_rows)

        main_keys_styles = [
            full_datetime_style,
            StatusStyle(),
            None,
        ]

        max_right_rows_cols = max_cols(right_rows)
        data_rows = join_tables(
            main_rows,
            middle_rows,
            right_rows,
            original_details_rows,
        )

        # Write row data.
        adaptive_value_style = ValueStyle()
        adaptive_right_style = ValueStyle(
            fill = openpyxl.styles.PatternFill(
                # Light Orange
                start_color = 'FFEFD5',
                end_color = 'FFEFD5',
                fill_type = 'solid',
            ),
        )
        for row_data in data_rows:
            styles = main_keys_styles[:]

            # Middle, alternating keys and values.
            styles += [KeyStyle(), adaptive_value_style] * (max_middle_cols // 2)

            # Right side formatting without key name on row.
            styles += [adaptive_right_style] * max_right_rows_cols

            # Formatting for original column data
            styles += [None]

            excel_row = ExcelRow(
                row_data,
                styles = styles,
                pyvalues = row_data,
            )
            yield excel_row

        # legIdentifier section at bottom.
        yield ExcelRow(tuple())
        yield ExcelRow(
            ('legIdentifier',),
            styles = [header_style],
            merge = (1, 2),
        )
        for key, val in member_data['legIdentifier'].items():
            yield ExcelRow(
                (key, val),
                styles = [
                    KeyStyle(),
                    adaptive_value_style,
                ],
            )

        # userId
        yield ExcelRow(tuple())
        yield ExcelRow(
            ('userId', member_data['userId']),
            styles = [
                KeyStyle(),
                adaptive_value_style,
            ],
        )
