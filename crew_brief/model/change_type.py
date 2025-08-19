from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from .base import Base

class ChangeType(Base):
    """
    Type of change in history shadow models.
    """

    __tablename__ = 'change_type'

    id = Column(
        Integer,
        primary_key = True,
    )

    name = Column(
        String,
        unique = True,
        nullable = False,
    )

    description = Column(
        Text,
        nullable = False,
    )
