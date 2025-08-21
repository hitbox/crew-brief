from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

class IgnoreFile(TimestampMixin, NonEmptyStringMixin, Base):
    """
    File path excluded from saving/indexing.
    """

    __tablename__ = 'ignore_file'

    id = Column(Integer, primary_key=True)

    path = Column(String, nullable=False, unique=True)
