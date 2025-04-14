from crew_brief.convert import bake_list
from crew_brief.mixin import ItemMixin

class EventDetail(ItemMixin):
    """
    Container for the unpredictable eventDetails dict from JSON.
    """

    __excel_filter__ = {
        ('minutes', 'fuel'): lambda data: data['minutes'] > 0 and data['fuel'] > 0
    }

    # If the tuple of keys are present in the dict value for a key, call func
    # to format the dict-value for Excel.
    __excel_format__ = {
        ('name', 'rank'): '{rank}: {name}'.format,
        ('minutes', 'fuel'): '{fuel}@{minutes} min.'.format,
    }

    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, val)

    def _excel_filter(self, key):
        """
        Decide if key should be included for Excel.
        """
        value = self[key]

        if value is None:
            # Refuse None (null) values.
            return False

        if isinstance(value, (dict, list, str, tuple)) and not value:
            # Refuse empty containers.
            return False

        if isinstance(value, dict):
            # Refuse specific dict-value for specific values.
            for keys, filter_ in self.__excel_filter__.items():
                if all(key in value for key in keys):
                    return filter_(value)

        return True

    def _excel_value(self, key):
        """
        Final formatting of Python values for Excel.
        """
        value = self[key]
        if isinstance(value, dict):
            for keys, formatter in self.__excel_format__.items():
                if all(key in value for key in keys):
                    value = formatter(**value)
                    break
        elif isinstance(value, (list, tuple)):
            value = bake_list(value)
        return value

    def __excel__(self):
        data = {}
        for key, val in self.items():
            if self._excel_filter(key):
                data[key] = self._excel_value(key)

        data = {key: data[key] for key in sorted(data)}
        return self.__class__(data)
