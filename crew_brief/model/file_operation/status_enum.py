from enum import IntEnum

from crew_brief.model.base import DatabaseEnumMeta

class FileOperationStatusEnum(
    IntEnum,
    metaclass = DatabaseEnumMeta,
):
    """
    Python side file operation status values.
    """

    __model__ = 'FileOperationStatus'

    CREATED = 1
    PENDING = 2
    IN_PROGRESS = 3
    SUCCESS = 4
    FAIL = 5

    __member_args__ = {
        'CREATED': {
            'description': 'Operation has been created.',
            'incoming_transitions': [],
            'outgoing_transitions': [PENDING],
        },
        'PENDING': {
            'description': 'Operation is waiting to be processed.',
            'incoming_transitions': [CREATED],
            'outgoing_transitions': [IN_PROGRESS],
        },
        'IN_PROGRESS': {
            'description': 'Operation is currently running.',
            'incoming_transitions': [PENDING],
            'outgoing_transitions': [
                SUCCESS,
                FAIL,
            ],
        },
        'SUCCESS': {
            'description': 'Operation completed successfully.',
            'incoming_transitions': [IN_PROGRESS],
            'outgoing_transitions': [],
        },
        'FAIL': {
            'description': 'Operation failed.',
            'incoming_transitions': [IN_PROGRESS],
            'outgoing_transitions': [PENDING],
        },
    }

    @classmethod
    def get_model(cls):
        from .status import FileOperationStatus
        return FileOperationStatus

    def db_instance(self, session):
        """
        Create a database instance from this (self) member.
        """
        from .status_transition import FileOperationStatusTransition

        model = self.get_model()

        def _db_objects(members):
            # Convert enum members to db objects.
            for member in members:
                instance = member.db_object(session)
                if instance:
                    yield instance

        instance = model(
            id = self.value,
            name = self.name,
            description = self.description,
        )

        # Add instance to session because the following may autoflush for
        # lookups.
        session.add(instance)

        for status in _db_objects(self.incoming_transitions):
            transition = FileOperationStatusTransition(
                from_status = status,
                to_status = instance,
            )
            instance.incoming_transitions.append(transition)

        for status in _db_objects(self.outgoing_transitions):
            transition = FileOperationStatusTransition(
                from_status = instance,
                to_status = status,
            )
            instance.outgoing_transitions.append(transition)

        return instance
