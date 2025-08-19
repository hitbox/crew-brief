from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from crew_brief.model.base import Base
from crew_brief.model.mixin import ShadowHistoryMixin
from crew_brief.model.mixin import TimestampMixin

from .status_enum import FileOperationStatusEnum

class FileOperation(
    ShadowHistoryMixin,
    TimestampMixin,
    Base,
):
    """
    An operation to perform on a file or files.
    """

    __tablename__ = 'file_operation'

    id = Column(
        Integer,
        primary_key = True,
    )

    leg_file_id = Column(
        Integer,
        ForeignKey('leg_file.id'),
        nullable = False,
    )

    leg_file = relationship(
        'LegFile',
        foreign_keys = f'FileOperation.leg_file_id',
    )

    operation_type_id = Column(
        Integer,
        ForeignKey('file_operation_type.id'),
        nullable = False,
    )

    operation_type = relationship(
        'FileOperationType',
        doc = 'Type of file operation to carry out.',
    )

    status_id = Column(
        Integer,
        ForeignKey('file_operation_status.id'),
        nullable = False,
        default = FileOperationStatusEnum.CREATED,
    )

    status = relationship(
        'FileOperationStatus',
        doc = 'Status of this file operation.',
    )

    @validates('status')
    def validate_status_transition(self, key, new_status):
        """
        Validate status transition to new status.
        """
        if self.status is not None and new_status not in self.status.to_statuses:
            raise ValueError(
                f'Invalid status transition from'
                f' {self.status.name} to {new_status.name}.'
            )
        return new_status

    enabled_at = Column(
        DateTime,
        nullable = True,
        doc = 'If not null, this file operation is enabled for processing.',
    )

    target_file_id = Column(
        Integer,
        ForeignKey('leg_file.id'),
        nullable = False,
    )

    target_file = relationship(
        'LegFile',
        foreign_keys = f'FileOperation.target_file_id',
        doc = 'The "other" file for this file operation.',
    )

    file_operation_associations = relationship(
        'FileOperationAssociation',
        back_populates = 'file_operation',
        cascade = 'all, delete-orphan',
        collection_class = ordering_list(
            'FileOperationAssociation.position'
        ),
    )

    files = association_proxy(
        'file_operation_associations',
        'leg_file',
    )

    # ShadowHistoryMixin
    history = relationship(
        'FileOperationHistory',
        back_populates = 'file_operation',
        cascade = 'all, delete-orphan',
        passive_deletes = True,
    )


def get_current_user(session):
    current_user = session.info.get('current_user')
    if not current_user:
        raise RuntimeError('Missing current_user')
    return current_user
