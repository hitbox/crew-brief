from enum import IntEnum

from crew_brief.model.base import DatabaseEnumMeta

class UserTypeEnum(IntEnum, metaclass=DatabaseEnumMeta):
    """
    UserType for Python side.
    """

    __model__ = 'UserType'

    BOT = 1
    HUMAN = 2

    @classmethod
    def get_model(cls):
        return UserType

    def db_instance(self):
        model = self.get_model()
        return model(
            id = self.value,
            name = self.name,
        )

    def to_user_type(self):
        return UserType(
            id = self.value,
            name = self.name,
        )
