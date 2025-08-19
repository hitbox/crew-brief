from enum import IntEnum

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from crew_brief.util import load_from_path

from .base import Base
from .mixin import ByMixin
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

class LegFileScrapeStatusEnum(IntEnum):
    """
    Enum for the status of the process of parsing LegFile object paths.
    """

    # 1. Filename regex matching.
    NO_MATCH = 1
    MATCH = 2

    # 2. Optional extra parsing to add string data to match data.
    NO_POSTMATCH = 3
    POSTMATCH = 4
    POSTMATCH_EXCEPTION = 5

    # 3. Schema
    DESERIALIZE = 6
    DESERIALIZE_EXCEPTION = 7

    # 4. Existing or new LegIdentifier object construction.
    LEG_IDENTIFIER = 8
    LEG_IDENTIFIER_EXCEPTION = 9


class LegFileScrapeStatus(Base):

    __tablename__ = 'leg_file_scrape_status'

    id = Column(Integer, primary_key=True)


class LegFileScrape(
    Base,
    ByMixin,
    NonEmptyStringMixin,
    TimestampMixin,
):
    """
    """

    __tablename__ = 'leg_file_scrape'

    id = Column(Integer, primary_key=True)

    name = Column(
        String,
        nullable = False,
        unique = True,
    )

    description = Column(
        Text,
        nullable = True,
    )

    leg_file_id = Column(
        Integer,
        ForeignKey('leg_file.id'),
        nullable = False,
    )

    leg_file = relationship(
        'LegFile',
    )

    status_id = Column(
        Integer,
        ForeignKey('leg_file_scrape_status.id'),
        nullable = False,
    )

    status = relationship(
        'LegFileScrapeStatus',
    )

    scraper_id = Column(
        Integer,
        ForeignKey('scraper.id'),
        nullable = False,
    )

    scraper = relationship(
        'Scraper',
    )

    matched_regex_id = Column(
        Integer,
        ForeignKey('regex.id'),
        nullable = True,
    )

    matched_regex = relationship(
        'Regex',
    )
