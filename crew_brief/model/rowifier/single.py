from crew_brief.sorting import join_tables
from crew_brief.sorting import max_cols

from .excel_row import ExcelRow
from .mixin import ConsistencyMixin

class SingleRowifier(ConsistencyMixin):
    """
    Produce key-value rows for output.
    """

    def __init__(
        self,
        row_splitter,
        header_style = None,
        main_keys_styles = None,
        key_style = None,
        middle_value_style = None,
        right_value_style = None,
    ):
        self.row_splitter = row_splitter
        self.header_style = header_style
        self.main_keys_styles = main_keys_styles
        self.key_style = key_style
        self.middle_value_style = middle_value_style
        self.right_value_style = right_value_style

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
            [self.header_style] * len(self.row_splitter.main_keys)
            # Middle, eventDetails header with merge for max row
            + [self.header_style] + [None] * (len(middle_header) - 1)
            # Right side of eventDetails
            + [self.header_style] * len(self.row_splitter.right_side_keys)
            # Original
            + [self.header_style]
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

        assert all(len(row) == 3 for row in main_rows)

        # Yield formatted data rows.
        max_right_rows_cols = max_cols(right_rows)
        data_rows = join_tables(
            main_rows,
            middle_rows,
            right_rows,
            original_details_rows,
        )

        # Write row data.
        for row_data in data_rows:
            styles = []

            if self.main_keys_styles:
                if len(self.main_keys_styles) != len(self.row_splitter.main_keys):
                    raise ValueError(
                        'main_keys_styles must be the same length as the'
                        ' splitter for main keys.')
                styles.extend(self.main_keys_styles)
            else:
                styles.extend([None] * len(self.row_splitter.main_keys))

            # Middle, alternating keys and values.
            if self.key_style and self.middle_value_style:
                styles += [self.key_style, self.middle_value_style] * (max_middle_cols // 2)
            else:
                styles += [None, None] * (max_middle_cols // 2)

            # Right side formatting without key name on row.
            if self.right_value_style:
                #styles += [self.right_value_style] * max_right_rows_cols
                styles.extend(self.right_value_style)
            else:
                styles += [None] * max_right_rows_cols

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
            styles = [self.header_style],
            merge = (1, 2),
        )
        for key, val in member_data['legIdentifier'].items():
            yield ExcelRow(
                (key, val),
                styles = [
                    self.key_style,
                    self.middle_value_style,
                ],
            )

        # userId
        yield ExcelRow(tuple())
        yield ExcelRow(
            ('userId', member_data['userId']),
            styles = [
                self.key_style,
                self.middle_value_style,
            ],
        )
