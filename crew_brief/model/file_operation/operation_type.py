from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from crew_brief.model.base import Base
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin

class FileOperationType(TimestampMixin, NonEmptyStringMixin, Base):
    """
    The type of operation to do on the files.
    """

    __tablename__ = 'file_operation_type'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    description = Column(String, nullable=False)
