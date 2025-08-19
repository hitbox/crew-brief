from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import object_session
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from crew_brief.model.base import Base
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin

class FileOperationAssociation(Base):
    """
    Ordered list of files associated with a file operation. Basically the file
    arguments to the operation.
    """

    __tablename__ = 'file_operation_association'

    id = Column(
        Integer,
        primary_key = True,
    )

    file_operation_id = Column(
        Integer,
        ForeignKey('file_operation.id'),
        nullable = False,
    )

    file_operation = relationship(
        'FileOperation',
        back_populates = 'file_operation_associations',
    )

    leg_file_id = Column(
        Integer,
        ForeignKey('leg_file.id'),
        nullable = False,
    )

    leg_file = relationship(
        'LegFile',
        back_populates = 'file_operation_associations',
    )

    position = Column(
        Integer,
        nullable = False,
        doc = 'Ordering for leg_file relation.',
    )
