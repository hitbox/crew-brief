from operator import attrgetter
from operator import itemgetter

from markupsafe import Markup
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import select
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import CodePairMixin
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

keys_for_unique_leg_identifier = (
    'airline_id',
    'flight_number_id',
    'origin_date_id',
    'departure_airport_id',
    'destination_airport_id',
    'ofp_version',
    'datetime',
)

get_leg_identifier_unique_key_attrs = attrgetter(*keys_for_unique_leg_identifier)
get_leg_identifier_unique_key_items = itemgetter(*keys_for_unique_leg_identifier)

def origin_date_creator(origin_date):
    from .origin_date import OriginDate
    return OriginDate(origin_date=origin_date)

def flight_number_creator(flight_number):
    from .flight_number import FlightNumber
    return FlightNumber(flight_number=flight_number)

class LegIdentifier(Base, TimestampMixin, NonEmptyStringMixin):
    """
    Uniquely identify a flight leg.
    """

    __tablename__ = 'leg_identifier'

    id = Column(Integer, primary_key=True)

    airline_id = Column(Integer, ForeignKey('airline.id'))
    airline = relationship(
        'Airline',
        back_populates = 'leg_identifiers',
    )
    airline_iata = association_proxy('airline', 'iata_code')
    airline_icao = association_proxy('airline', 'icao_code')

    flight_number_id = Column(Integer, ForeignKey('flight_number.id'))
    flight_number_object = relationship(
        'FlightNumber',
    )
    flight_number = association_proxy(
        'flight_number_object',
        'flight_number',
        creator = flight_number_creator,
    )

    origin_date_id = Column(Integer, ForeignKey('origin_date.id'))
    origin_date_object = relationship(
        'OriginDate',
    )
    origin_date = association_proxy(
        'origin_date_object',
        'origin_date',
        creator = origin_date_creator,
    )

    departure_airport_id = Column(Integer, ForeignKey('airport.id'))
    departure_airport = relationship(
        'Airport',
        foreign_keys = [departure_airport_id],
        back_populates = 'departure_leg_identifiers',
    )
    departure_airport_iata = association_proxy('departure_airport', 'iata_code')

    destination_airport_id = Column(Integer, ForeignKey('airport.id'))
    destination_airport = relationship(
        'Airport',
        foreign_keys = [destination_airport_id],
        back_populates = 'destination_leg_identifiers',
    )
    destination_airport_iata = association_proxy('destination_airport', 'iata_code')

    ofp_version = Column(
        String,
        nullable = True,
    )

    ofp_version_id = Column(
        Integer,
        ForeignKey('ofp_version.id'),
        nullable = True,
    )

    ofp_version_object = relationship(
        'OFPVersion',
    )

    datetime = Column(
        DateTime,
        nullable = True,
        doc = 'Unknown datetime that is often available from filenames.',
    )

    leg_file = relationship(
        'LegFile',
        doc = 'The file that was scraped to produce this record.',
        back_populates = 'leg_identifier',
    )

    scraped_by_id = Column(Integer, ForeignKey('scraper.id'))

    scraped_by = relationship(
        'Scraper',
        doc = 'The object that produced this record of leg identifier info.',
    )

    # matching_files relationship() in __init__

    # TODO
    # - expression for complete leg_identifier, especially for origin_date_object

    @classmethod
    def get_or_create_from_parse(
        cls,
        session,
        airline,
        flight_number,
        origin_date,
        departure_airport,
        destination_airport,
        ofp_version_object,
        datetime,
    ):
        """
        Get or create from data available from parsing. See crew_brief.parse.
        """
        stmt = (
            select(cls)
            .where(
                cls.airline == airline,
                cls.flight_number_object == flight_number,
                cls.origin_date_object == origin_date,
                cls.departure_airport == departure_airport,
                cls.destination_airport == destination_airport,
                cls.ofp_version_object == ofp_version_object,
                cls.datetime == datetime,
            )
        )
        instance = session.scalars(stmt).one_or_none()
        if instance is None:
            instance = cls(
                airline = airline,
                flight_number_object = flight_number,
                origin_date_object = origin_date,
                departure_airport = departure_airport,
                destination_airport = destination_airport,
                ofp_version_object = ofp_version_object,
                datetime = datetime,
            )
            session.add(instance)
        return instance

    def as_parts(self):
        parts = [
            self.airline_iata,
            self.flight_number,
            self.departure_airport.iata_code,
            self.destination_airport.iata_code,
        ]
        if self.origin_date:
            parts.append(self.origin_date.strftime('%d%b%y'))
        else:
            parts.append('(None)')
        if self.ofp_version_object is not None:
            parts.append(self.ofp_version_object)
        else:
            parts.append('(None)')
        return parts

    @property
    def short_name(self):
        parts = self.as_parts()
        return ' '.join(map(str, parts))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f'< not supported for {other}')

        return leg_identifier_key(self) < leg_identifier_key(other)

    def __html__(self):
        return Markup(f'<pre class="data">{ self.short_name }</pre>')
