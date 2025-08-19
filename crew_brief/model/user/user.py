from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import object_session
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from crew_brief.model.base import Base
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin

class User(NonEmptyStringMixin, TimestampMixin, Base):
    """
    A user of this, crew_brief system.
    """

    __tablename__ = 'user'

    id = Column(
        Integer,
        primary_key = True,
    )

    username = Column(
        String,
        nullable = False,
        unique = True,
    )

    realname = Column(
        String,
        nullable = False,
    )

    user_type_id = Column(
        ForeignKey('user_type.id'),
        nullable = False,
    )

    user_type = relationship(
        'UserType',
    )
