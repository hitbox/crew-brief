class ExcelRow:

    def __init__(self, values, styles=None, merge=None, pyvalues=None):
        self.values = values
        self.styles = styles
        self.merge = merge
        self.pyvalues = pyvalues or values

    def __iter__(self):
        return iter(map(for_excel, self.values))

    def __len__(self):
        return len(self.values)

    def apply_styles(self, ws, row):
        # Would really like strict here, but worksheets are weird and some rows
        # come back with many extra None values.
        items = zip(ws[row], self.styles, self.pyvalues)
        for cell, style, pyvalue in items:
            if style:
                # Consider StyleClass
                if callable(style):
                    style(cell, pyvalue)
                else:
                    for key, val in style.items():
                        setattr(cell, key, val)

    def apply_merges(self, ws, row):
        start_column, end_column = self.merge
        ws.merge_cells(
            start_row = row,
            start_column = start_column,
            end_row = row,
            end_column = end_column,
        )

    def apply(self, ws, row=None):
        """
        Apply styling to worksheet row, defaulting to the last row.
        """
        if row is None:
            row = ws.max_row
        if self.merge:
            self.apply_merges(ws, row)
        if self.styles:
            self.apply_styles(ws, row)


def for_excel(value):
    if hasattr(value, '__excel__'):
        return value.__excel__()
    elif isinstance(value, dict):
        return str(value)
    return value
