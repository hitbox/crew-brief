from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import CodePairMixin
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

class Airline(Base, CodePairMixin, TimestampMixin, NonEmptyStringMixin):

    __tablename__ = 'airline'

    id = Column(Integer, primary_key=True)

    leg_identifiers = relationship(
        'LegIdentifier',
        back_populates = 'airline',
    )
