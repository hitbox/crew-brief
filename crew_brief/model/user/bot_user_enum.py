from crew_brief.model.base import DatabaseEnumMeta
from crew_brief.model.base import DatabaseIntEnumBase

class BotUserEnum(DatabaseIntEnumBase, metaclass=DatabaseEnumMeta):
    """
    Robot user accounts required to exist for automation.
    """

    __model__ = 'User'

    SEEDBOT = 1
    PARSEBOT = 2
    UPDATEBOT = 3
    PLANBOT = 4

    __member_args__ = {
        'SEEDBOT': {
            'username': 'seedbot',
            'realname': 'system',
        },
        'PARSEBOT': {
            'username': 'parsebot',
            'realname': 'system',
        },
        'UPDATEBOT': {
            'username': 'updatebot',
            'realname': 'system',
        },
        'PLANBOT': {
            'username': 'planbot',
            'realname': 'system',
        },
    }

    @classmethod
    def get_model(cls):
        from .user import User
        return User

    def db_instance(self, user_type):
        model = self.get_model()
        instance = model(
            id = self.value,
            username = self.username,
            realname = self.realname,
            user_type = user_type
        )
        return instance
