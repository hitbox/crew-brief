"""
Convert strings to types.
"""
import datetime

from . import constants

NB_SPACE = '\xa0'

class DateTimeConverter:
    """
    Callable tries to convert a string to a datetime against many formats.
    """

    def __init__(self, *formats):
        self.formats = formats

    def __call__(self, string):
        for format_ in self.formats:
            try:
                return datetime.datetime.strptime(string, format_)
            except (TypeError, ValueError):
                pass
        return None


class DateConverter(DateTimeConverter):
    """
    Callable tries to convert a string to a date object.
    """

    def __call__(self, string):
        dt = super().__call__(string)
        if dt:
            return dt.date()
        return None


class FloatConverter:
    """
    Callable tries to convert a string to a float.
    """

    def __call__(self, string):
        try:
            return float(string)
        except (TypeError, ValueError):
            pass
        return None


class IntegerConverter:
    """
    Callable tries to convert a string to an integer.
    """

    def __call__(self, string):
        try:
            return int(string)
        except (TypeError, ValueError):
            pass
        return None


class TypeConverter:
    """
    Callable tries to convert a string to a data type.
    """

    def __init__(self, *funcs):
        self.funcs = funcs

    def __call__(self, value):
        """
        Try convert to data type.
        """
        if value is None:
            return None

        for func in self.funcs:
            result = func(value)
            if result is not None:
                return result

        return value


# Important order, especially for int and float.
def default_converter():
    type_converter = TypeConverter(
        DateTimeConverter(
            constants.ZDATETIME_FORMAT,
        ),
        IntegerConverter(),
        FloatConverter(),
    )
    return type_converter

def deep_convert(data, converter=None):
    """
    Recursively try to update types.
    """
    # Raise for not implemented.
    if isinstance(data, tuple):
        raise NotImplementedError('tuple')
    if isinstance(data, set):
        raise NotImplementedError('set')

    if converter is None:
        converter = default_converter()

    if not isinstance(data, (dict, list)):
        # Convert for non-container.
        return converter(data)
    else:
        # Update items in container from recursion.
        if isinstance(data, dict):
            items = data.items()
        elif isinstance(data, list):
            items = enumerate(data)

        for key, value in items:
            if isinstance(value, str):
                typed = deep_convert(value, converter)
                if typed is not None:
                    data[key] = typed

def bake_list(value):
    """
    Make a nice string for lists.
    """
    if len(value) > 1:
        return '\n'.join(f'• {thing}' for thing in value)
    return str(value[0])


def to_excel_value(value):
    """
    Convert value for Excel.
    """
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            return value[0]
        elif len(value) > 1:
            return bake_list(value)
        else:
            return value

    if isinstance(value, dict):
        return str(value)

    if isinstance(value, set):
        return str(value)

    if isinstance(value, str):
        # Strip whitespace.
        value = value.strip()
        if constants.NESTED_KEY_SEP in value:
            # Split into newlines and make spaces between splits
            # non-breaking.
            def nbsp(word):
                return word.replace(' ', NB_SPACE)
            words = value.split(constants.NESTED_KEY_SEP)
            words = (nbsp(word) for word in words)
            value = '\n'.join(words)

    return value
