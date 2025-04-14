import datetime

import openpyxl

from crew_brief.output.excel import ExcelConverter
from crew_brief.output.excel import muted_blue_fill

header_style = ExcelConverter.styles['header_style']
full_datetime_style = ExcelConverter.styles['full_datetime_style']
full_datetime_style = ExcelConverter.styles['full_datetime_style']

id_keys = set([
    'receivedFrom',
    'sharedWithDevice',
    'submittedBy',
    'sentTo',
    'receivedFromDevice',
    'userId',
])

class StatusStyle:

    def __call__(self, cell, pyvalue):
        if cell.value == 'success':
            name = 'success_style'
        else:
            name = 'not_success_style'
        for key, val in ExcelConverter.styles[name].items():
            setattr(cell, key, val)


class ValueStyle:
    """
    Apply Excel cell formatting for Python values.
    """

    def __init__(self, **extra):
        self.extra = extra

    def __call__(self, cell, pyvalue):
        worksheet = cell.parent
        if isinstance(pyvalue, list):
            # Format cell for formatted list string.
            cell.alignment = openpyxl.styles.Alignment(
                wrap_text = True,
            )
        elif isinstance(pyvalue, datetime.datetime):
            # Format datetime
            cell.number_format = 'yyyy-mm-dd hh:mm:ssZ'
        elif isinstance(pyvalue, datetime.date):
            # Format date
            cell.number_format = 'yyyy-mm-dd'
        elif isinstance(pyvalue, int):
            left_cell = worksheet.cell(row=cell.row, column=cell.column - 1)
            if left_cell.value not in id_keys:
                cell.number_format = '#,##0'
        elif isinstance(pyvalue, float):
            cell.number_format = '#,##0.00'

        if pyvalue:
            for key, value in self.extra.items():
                setattr(cell, key, value)


class KeyStyle:

    def __call__(self, cell, pyvalue):
        if pyvalue is not None:
            cell.fill = muted_blue_fill
            cell.font = openpyxl.styles.Font(
                bold = True,
            )
