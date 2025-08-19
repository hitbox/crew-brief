from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import CodePairMixin
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

class Airport(Base, CodePairMixin, TimestampMixin, NonEmptyStringMixin):

    human_description = 'IATA and ICAO airport codes.'

    __tablename__ = 'airport'

    id = Column(Integer, primary_key=True)

    departure_leg_identifiers = relationship(
        'LegIdentifier',
        foreign_keys = 'LegIdentifier.departure_airport_id',
        back_populates = 'departure_airport',
    )

    destination_leg_identifiers = relationship(
        'LegIdentifier',
        foreign_keys = 'LegIdentifier.destination_airport_id',
        back_populates = 'destination_airport',
    )

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f'< with {other} is not supported')
        # TODO
        return self.id < other.id

    def __html__(self):
        return self.iata_code
