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
default_converter = TypeConverter(
    DateTimeConverter(
        constants.ZDATETIME_FORMAT,
    ),
    IntegerConverter(),
    FloatConverter(),
)


def rtype_update(data, converter=None):
    if converter is None:
        converter = default_converter

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = converter(value)
    elif isinstance(data, (list, tuple)):
        for index, item in enumerate(data):
            if isinstance(value, str):
                data[index] = converter(value)
