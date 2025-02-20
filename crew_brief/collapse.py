class DataKeyCollapse:
    """
    Collapse in-place, data with keys that are values into a single value.
    """
    # XXX: Consider an expand-data-key callable?

    def __init__(self, *keys):
        self.keys = keys

    def __call__(self, data):
        """
        Reshape data having values as keys.

        Ex.: {assignedTakeOffDuty: {'CA': '(Name of person)'}}

        As far as I know, these are always a single entry dict but just in case
        we'll join each item.
        """
        for key in self.keys:
            if key in data:
                new_value = ', '.join(' '.join(item) for item in data.items())
                data[key] = new_value


class EventTypeVersionedCollapse:
    """
    Modify data in-place for versioned keys that are not different.
    """

    def __init__(self, event_type_mapping):
        self.event_type_mapping = event_type_mapping

    def __call__(self, event_type, event_details):
        if new_old_keys := self.event_type_mapping.get(event_type):
            for new_key, old_key in new_old_keys:
                new_val = event_details[new_key]
                old_val = event_details[old_key]
                if new_val == old_val:
                    del event_details[new_key]
                    del event_details[old_key]
