from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from crew_brief.model.base import Base
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin

class FileOperationStatus(
    TimestampMixin,
    NonEmptyStringMixin,
    Base,
):
    """
    Current status of a file operation.
    """

    __tablename__ = 'file_operation_status'

    id = Column(
        Integer,
        primary_key = True,
    )

    name = Column(
        String,
        nullable = False,
        unique = True,
    )

    description = Column(
        String,
        nullable = False,
    )

    incoming_transitions = relationship(
        'FileOperationStatusTransition',
        foreign_keys = 'FileOperationStatusTransition.to_status_id',
        back_populates = 'to_status',
        cascade = 'all, delete-orphan',
    )

    from_statuses = association_proxy(
        'incoming_transitions',
        'from_status',
    )

    outgoing_transitions = relationship(
        'FileOperationStatusTransition',
        foreign_keys = 'FileOperationStatusTransition.from_status_id',
        back_populates = 'from_status',
        cascade = 'all, delete-orphan',
    )

    to_statuses = association_proxy(
        'outgoing_transitions',
        'to_status',
    )
