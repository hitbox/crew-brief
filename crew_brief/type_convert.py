"""
Convert strings to types.
"""
import datetime

from . import constants

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


class FloatConverter:
    """
    Callable tries to convert a string to a float.
    """

    def __call__(self, string):
        try:
            return float(string)
        except (TypeError, ValueError):
            pass


class IntegerConverter:
    """
    Callable tries to convert a string to an integer.
    """

    def __call__(self, string):
        try:
            return int(string)
        except (TypeError, ValueError):
            pass


class TypeConverter:
    """
    Callable tries to convert a string to a data type.
    """

    def __init__(self, *funcs):
        self.funcs = funcs

    def __call__(self, string):
        """
        Try convert to data type.
        """
        for func in self.funcs:
            result = func(string)
            if result is not None:
                return result
        return string


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

def rtype_update(data, converter=None):
    """
    Recursively try to update types.
    """
    if converter is None:
        converter = default_converter()

    if isinstance(data, (dict, list)):
        if isinstance(data, dict):
            items = data.items()
        elif isinstance(data, list):
            items = enumerate(data)
        for key, value in items:
            if isinstance(value, str):
                typed = rtype_update(value, converter)
                if typed is not None:
                    data[key] = typed
    elif isinstance(data, tuple):
        raise NotImplementedError('tuple')
    elif isinstance(data, set):
        raise NotImplementedError('set')
    else:
        return converter(data)
