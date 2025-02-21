from operator import itemgetter

import openpyxl

from crew_brief import rowifier
from crew_brief import sorting

def new_from(instance, class_, **kwargs):
    # Work around for creating immutable openpyxl Alignment objects.
    oldkw = {k:v for k, v in instance.__dict__.items() if k not in kwargs}
    return class_(**kwargs, **oldkw)

class ExcelConverter:
    """
    Convert UserEvents JSON to Excel.
    """

    header = ['eventTimeStamp', 'status', 'eventType', 'eventDetails']
    first_three = header[:3]

    identifier_keys = set([
        'userId',
        'submittedBy',
    ])

    styles = dict(
        header_style = dict(
            font = openpyxl.styles.Font(
                bold = True,
            ),
            alignment = openpyxl.styles.Alignment(
                vertical = 'top',
                horizontal = 'center',
            ),
        ),
        key_style = dict(
            font = openpyxl.styles.Font(
                bold = True,
            ),
            alignment = openpyxl.styles.Alignment(
                vertical = 'top',
            ),
        ),
        not_success_style = dict(
            font = openpyxl.styles.Font(
                color = 'FFFFFF',
                bold = True,
            ),
            fill = openpyxl.styles.PatternFill(
                start_color = 'FF0000',
                end_color = 'FF0000',
                fill_type = 'solid',
            ),
        ),
        list_style = dict(
            alignment = openpyxl.styles.Alignment(
                wrap_text = True,
            ),
        ),
        event_details_header_style = dict(
            alignment = openpyxl.styles.Alignment(
                horizontal = 'center',
            ),
        ),
        integer_style = dict(
            number_format = '#,##0',
        ),
        datetime_style = dict(
            number_format = 'yyyy-mm-dd hh:mm',
        ),
        waypoint_style = dict(
            font = openpyxl.styles.Font(
                bold = True,
            ),
            fill = openpyxl.styles.PatternFill(
                start_color = 'FFFF00',
                end_color = 'FFFF00',
                fill_type = 'solid',
            ),
        ),
        identifier_style = dict(
            alignment = openpyxl.styles.Alignment(
                horizontal = 'left',
            ),
        ),
    )

    def __init__(self):
        self.style_names = [name for name in dir(self) if name.endswith('_style')]
        self.iter_flattened = rowifier.SingleRowIterator()
        self.iter_doubled = rowifier.DoubledRowIterator()
        self.important_keys = sorting.EventDetailsKey()

    def apply_style(self, cell, style):
        for attr, val in style.items():
            setattr(cell, attr, val)

    def autofit_columns(self, ws, padding=2):
        for col in ws.columns:
            max_length = 0
            col_letter = None
            for cell in col:
                if isinstance(cell, openpyxl.cell.cell.MergedCell):
                    continue
                if col_letter is None:
                    col_letter = cell.column_letter
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))

            # Add some padding
            ws.column_dimensions[col_letter].width = max_length + padding

    def autofit_rows(self, ws):
        # Auto-fit row height based on newline count
        for row in ws.iter_rows():
            max_lines = max(str(cell.value).count("\n") + 1 if cell.value else 1 for cell in row)
            # Adjust factor as needed
            ws.row_dimensions[row[0].row].height = max_lines * 15

    def merge_for_bottom(self, ws):
        ws.merge_cells(
            start_row = ws.max_row,
            start_column = 2,
            end_row = ws.max_row,
            end_column = ws.max_column,
        )

    def to_excel(self, path_data, data):
        wb = openpyxl.Workbook()
        ws = wb.active

        # Freeze header row.
        ws.freeze_panes = 'A2'

        # User Events
        header = ['eventTimeStamp', 'status', 'eventType', 'eventDetails']
        status_index = header.index('status')
        status_column = status_index + 1

        ws.append(header)

        # Style the header.
        for cell in ws[ws.max_row]:
            self.apply_style(cell, self.styles['header_style'])

        # Write user events.
        for user_event in data['userEvents']:
            row = self.get_first_three(user_event)
            status = row[status_index]
            success = status == 'success'

            # Init dict of style attribute names to list of columns the styles
            # are applied to.
            column_styles = dict(
                key_style = [1, 2, 3],
            )
            for style_name in self.styles:
                column_styles[style_name] = []
                if not success:
                    column_styles[style_name].append(status_column)

            if event_details := user_event.get('eventDetails'):
                for parents, value in visit_for_dict(event_details, key_sort=self.important_keys):
                    # Save some useful column numbers.
                    key_column = len(row) + 1
                    value_column = key_column + 1

                    # Add key cell to list to make bold.
                    column_styles['key_style'].append(key_column)

                    # Handle weirdly structured data where keys are actually
                    # data values.
                    if parents[0] in self.weird_keys:
                        # Ex.: {assignedTakeOffDuty: {'CA': '(Name of person)'}}
                        value = ' '.join([parents[1], value])
                        parents = (parents[0], )

                    elif parents[0] in (self.fuel_keys):
                        if parents[1] == 'fuel':
                            # Remove redundant key.
                            parents = (parents[0], )
                        else:
                            # Add extra information to key cell.
                            parents = (parents[0], ) + tuple(key.capitalize() for key in parents[1:])

                    elif parents[0] == 'waypoint':
                        column_styles['waypoint_style'].extend((key_column, value_column))

                    if isinstance(value, (list, tuple)) and value:
                        # A populated list or tuple.
                        # Newline separated for populated lists and tuples
                        # and add to columns to make text wrap.
                        value = '\n'.join(f'● {thing}' for thing in value)
                        # Add value cell to be formatted as a list.
                        column_styles['list_style'].append(value_column)
                    if int_value := self.try_integer(value):
                        value = int_value
                        if parents[0] in self.identifier_keys:
                            column_styles['identifier_style'].append(value_column)
                        else:
                            column_styles['integer_style'].append(value_column)
                    elif float_value := self.try_float(value):
                        value = float_value
                    elif datetime_value := self.try_datetime(value):
                        value = datetime_value
                        column_styles['datetime_style'].append(value_column)
                    else:
                        value = str(value)

                    # Add cells to end of row.
                    key_value = ' '.join(f'{key}' for key in parents)
                    row += (key_value, value)

            # Add constructed row and style its cells.
            ws.append(row)
            for cell in ws[ws.max_row]:
                for style_name, columns in column_styles.items():
                    if cell.column in columns:
                        self.apply_style(cell, self.styles[style_name])

                cell.alignment = new_from(
                    cell.alignment,
                    openpyxl.styles.Alignment,
                    vertical = 'top',
                )

        # Write the original event details. Wait until nested data is written
        # to find the rightmost column.
        column = ws.max_column + 1
        for row, user_event in enumerate(data['userEvents'], start=2):
            if 'eventDetails' in user_event:
                event_details = user_event['eventDetails']
                ws.cell(row=row, column=column, value=str(event_details))

        # Merge eventDetails column across expanded key-values cells. Wait
        # until all columns written.
        ws.merge_cells(
            start_row = 1,
            start_column = 4,
            end_row = 1,
            end_column = ws.max_column,
        )
        self.apply_style(ws.cell(row=1, column=4), self.styles['event_details_header_style'])

        # Hide the JSON data in last column.
        ws.column_dimensions[
            openpyxl.utils.get_column_letter(ws.max_column)
        ].hidden = True

        # Bottom.
        ws.append(('legIdentifier', data['legIdentifier']))
        self.merge_for_bottom(ws)
        ws.append(('userId', int(data['userId'])))
        self.apply_style(ws.cell(row=ws.max_row, column=2), self.styles['identifier_style'])
        self.merge_for_bottom(ws)

        # Autofit rows and columns.
        self.autofit_columns(ws)
        self.autofit_rows(ws)

        return wb

    def apply_row_styles(self, cells, values):
        for cell, value in zip(cells, values):
            if isinstance(value, (list, tuple)):
                self.apply_style(cell, self.styles['list_style'])

    def __call__(
        self,
        path_data,
        user_events_data,
        original_user_events_data,
        flattened = False,
    ):
        """
        Convert UserEvents.txt JSON data to Excel.

        :param path_data: Data scraped from the path to the zip file.
        :param user_events_data: Original JSON data.
        """
        if flattened:
            row_iterator = self.iter_flattened
        else:
            row_iterator = self.iter_doubled

        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append(self.header)

        user_events = user_events_data['userEvents']
        original_user_events = original_user_events_data['userEvents']

        for row in row_iterator(user_events, original_user_events):
            ws.append(row)
            cells = ws[ws.max_row]
            self.apply_row_styles(cells, row)

        return wb


def bake_list(self, value):
    return '\n'.join(f'● {thing}' for thing in value)

def autofit_with_excel(filename):
    """
    Autofit columns and rows with Excel.
    """
    excel = win32.Dispatch('Excel.Application')
    filename = os.path.abspath(os.path.normpath(filename))
    wb = excel.Workbooks.Open(filename)
    ws = wb.ActiveSheet
    ws.Cells.Columns.AutoFit()
    ws.Cells.Rows.AutoFit()
    wb.Save()
