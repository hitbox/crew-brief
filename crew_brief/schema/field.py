import re

import marshmallow as mm

class DataStringField(mm.fields.Field):
    """
    Split string on separator and convert to dict.
    """

    def __init__(self, part_names, sep, part_types=None, **kwargs):
        """
        :param part_names:
            Ordered list of names for the parts of the string.
        :param sep:
            Separator.
        :param part_types:
            Dict of names to functions to apply to resulting split-dict.
        :param kwargs:
            Remaining keyword arguments to pass to parent field class.
        """
        self.part_names = part_names
        self.sep = sep
        self.part_types = part_types
        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Split string on separator and join names into a dict.
        """
        value_data = dict(zip(self.part_names, value.split(self.sep)))
        if self.part_types:
            for key, func in self.part_types.items():
                key_value = value_data[key]
                value_data[key] = func(key_value)
        return value_data


class IntOrStringField(mm.fields.Field):
    """
    Try make integer falling back to string.
    """

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, int):
            return value

        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return value

        raise mm.ValidationError("Invalid type: Must be a string or integer.")


class RegexField(mm.fields.Field):

    def _deserialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, str):
            raise mm.ValidationError('Expected string.')

        try:
            regex = re.compile(value)
        except re.error:
            raise mm.ValidationError('Invalid regex pattern.')

        return regex


class RegexListField(mm.fields.List):
    """
    Field assembles keys that match a regex, into values in a list.
    """

    def __init__(self, *args, pattern, **kwargs):
        self.regex = re.compile(pattern)
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, dict):
            raise ValueError('Expected dictionary.')
        return [key for key in value.keys() if self.regex.match(key)]
