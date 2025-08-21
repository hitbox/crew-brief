from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin
from .mixin import InstanceMixin

class FlightNumber(Base, TimestampMixin, NonEmptyStringMixin, InstanceMixin):
    """
    """

    __tablename__ = 'flight_number'

    id = Column(Integer, primary_key=True)

    flight_number = Column(String, nullable=False)

    leg_identifiers = relationship(
        'LegIdentifier',
        back_populates = 'flight_number_object',
    )

    @classmethod
    def creator(cls, flight_number):
        return cls(flight_number=flight_number)

    @classmethod
    def from_key_values(cls, flight_number):
        return cls(flight_number=flight_number)

    @classmethod
    def get_or_create_by_flight_number(cls, session, flight_number):
        instance = session.scalars(select(cls).where(cls.flight_number == flight_number)).one_or_none()
        if instance is None:
            instance = cls(flight_number=flight_number)
            session.add(instance)
        return instance

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f'< not supported for {other}')
        return self.flight_number < other.flight_number

    def __html__(self):
        return self.flight_number
