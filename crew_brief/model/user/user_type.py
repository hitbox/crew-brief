from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from crew_brief.model.base import Base
from crew_brief.model.mixin import NonEmptyStringMixin

class UserType(NonEmptyStringMixin, Base):
    """
    Type of user account object. Mainly to differentiate humans from bots.
    """

    __tablename__ = 'user_type'

    id = Column(
        Integer,
        primary_key = True,
    )

    name = Column(
        String,
        nullable = False,
    )

    users = relationship(
        'User',
        back_populates = 'user_type',
    )
