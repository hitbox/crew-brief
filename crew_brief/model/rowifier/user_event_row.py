class UserEventRow:
    """
    Wrap rowified userEvent object.
    """

    def __init__(self, style_hint, row, original, keys):
        self.style_hint = style_hint
        self.row = row
        self.original = original
        self.keys = keys

    def __len__(self):
        return len(self.row)

    def __iter__(self):
        yield self.style_hint
        yield self.row
        yield self.original
