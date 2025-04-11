import openpyxl

class Styling:
    """
    """

    def __init__(self, styles):
        self.styles = styles

    @classmethod
    def from_workbook(cls, filename, prefix):
        """
        Scrape styles from named cells in workbook and instantiate.
        """
        wb = openpyxl.load_workbook(filename)
        named = {
            name: defined_name
            for name, defined_name in wb.defined_names.items()
            if name.startswith(prefix)
        }
        styles = {}
        for name, defined_name in named.items():
            cell = [wb[sheet][address] for sheet, address in defined_name.destinations]
            if len(cell) < 1:
                raise ValueError(f'No cells for {name}.')
            elif len(cell) > 1:
                raise ValueError(f'More than one cell for {name}.')
            cell = cell[0]
            styles[name.removeprefix(prefix)] = cell
        return cls(styles)

    def __getitem__(self, key):
        return self.styles[key]
