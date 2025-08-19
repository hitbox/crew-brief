from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from crew_brief.model.base import Base
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin

class FileOperationStatusTransition(Base):
    """
    Valid file operation status transitions. What status may be transitioned to.
    """

    __tablename__ = 'file_operation_status_transition'

    from_status_id = Column(
        ForeignKey(
            'file_operation_status.id',
            ondelete = 'CASCADE',
        ),
        primary_key = True,
    )

    from_status = relationship(
        'FileOperationStatus',
        foreign_keys = [from_status_id],
        back_populates = 'outgoing_transitions',
    )

    to_status_id = Column(
        ForeignKey(
            'file_operation_status.id',
            ondelete = 'CASCADE',
        ),
        primary_key = True,
    )

    to_status = relationship(
        'FileOperationStatus',
        foreign_keys = [to_status_id],
        back_populates = 'incoming_transitions',
    )
