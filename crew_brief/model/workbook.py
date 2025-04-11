import io

import openpyxl

from crew_brief.type_convert import to_excel_value

class WorkbookBuilder:
    """
    """

    def __init__(self, rowifier):
        self.rowifier = rowifier

    def new_workbook(self):
        return openpyxl.Workbook()

    def __call__(self, path_data, data):
        """
        """
        wb = self.new_workbook()
        ws = wb.active

        for row in self.rowifier(data, data):
            row = tuple(map(to_excel_value, row))
            ws.append(row)

        with io.BytesIO() as excel_stream:
            wb.save(excel_stream)
            excel_data = excel_stream.getvalue()

        return excel_data
