from enum import IntEnum

from .base import DatabaseEnumMeta

class ChangeTypeEnum(IntEnum, metaclass=DatabaseEnumMeta):
    """
    ChangeType object for use on the Python side.
    """

    __model__ = 'ChangeType'

    INSERT = 1
    UPDATE = 2
    DELETE = 3

    __member_args__ = {
        'INSERT': {
            'description': 'New record created in source table.',
        },
        'UPDATE': {
            'description': 'One or more fields changed in source table.',
        },
        'DELETE': {
            'description': 'Record deleted in source table.',
        },
    }

    @classmethod
    def get_model(cls):
        return ChangeType

    def db_instance(self):
        model = self.get_model()
        return model(
            id = self.value,
            name = self.name,
        )
