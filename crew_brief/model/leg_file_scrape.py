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

class LegFileScraperHistory(
    Base,
    ByMixin,
    NonEmptyStringMixin,
    TimestampMixin,
):
    """
    Steps of scraping done by a Scraper against a LegFile.
    """

    __tablename__ = 'leg_file_scraper_history'

    id = Column(Integer, primary_key=True)

    leg_file_id = Column(
        Integer,
        ForeignKey('leg_file.id'),
        nullable = False,
    )

    leg_file = relationship(
        'LegFile',
    )

    scraper_step_id = Column(
        Integer,
        ForeignKey('scraper_step.id'),
        nullable = False,
    )

    scraper_step = relationship(
        'ScraperStep',
        doc = 'ScraperStep object for the scraping step that was done to this LegFile.',
    )

    exception_id = Column(
        Integer,
        ForeignKey('exception_instance.id'),
        nullable = True,
    )

    exception = relationship(
        'ExceptionInstance',
    )
