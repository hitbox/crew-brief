class Styler:
    """
    Apply styling function to cells.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, cell, pyvalue):
        self.func(cell, pyvalue)


class ConditionalStyle:
    """
    Style cell based on a condition with an option to style if condition fails
    too. By default the condition is that the cell is not none.
    """

    def __init__(self, style, else_style=None, condition=None):
        self.style = style
        self.else_style = else_style
        if condition is None:
            condition = lambda cell, pyvalue: pyvalue is not None
        self.condition = condition

    def apply(self, cell, style):
        for key, val in style.items():
            setattr(cell, key, val)

    def __call__(self, cell, pyvalue):
        if self.condition(cell, pyvalue):
            self.apply(cell, self.style)
        elif self.else_style:
            self.apply(cell, self.else_style)
