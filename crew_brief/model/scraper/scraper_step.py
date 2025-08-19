from enum import IntEnum

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from crew_brief.model.base import Base
from crew_brief.model.mixin import ByMixin
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin
from crew_brief.util import load_from_path

class ScraperStepTypeEnum(IntEnum):

    REGEX = 1
    SCHEMA = 2
    FUNCTION = 3


class ScraperStepType(Base):
    """
    Polymorphic step type.
    """

    __tablename__ = 'scraper_step_type'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)


class ScraperStep(Base):
    """
    One step in the scraping process whereby a LegIdentifier is created from a
    LegFile path.
    """

    __tablename__ = 'scraper_step'

    id = Column(Integer, primary_key=True)

    scraper_id = Column(ForeignKey('scraper.id'))

    scraper = relationship(
        'Scraper',
        back_populates = 'steps',
    )

    position = Column(Integer, nullable=False)

    type_id = Column(
        Integer,
        ForeignKey('scraper_step_type.id'),
        nullable = False
    )

    step_type = relationship(
        'ScraperStepType',
    )

    __mapper_args__ = {
        'polymorphic_on': type_id,
        'polymorphic_identity': 'base',
    }


class RegexStep(ScraperStep):
    """
    LegFile path capture group regex parser.
    """

    __tablename__ = 'scraper_step_regex'

    id = Column(Integer, ForeignKey('scraper_step.id'), primary_key=True)

    regex_id = Column(ForeignKey('regex.id'))

    regex = relationship('Regex')

    __mapper_args__ = {
        'polymorphic_identity': 'regex',
    }


class FunctionStep(ScraperStep):
    """
    Callable that adds more data to the group dict from the regex step.
    """

    __tablename__ = 'scraper_step_function'

    id = Column(Integer, ForeignKey('scraper_step.id'), primary_key=True)

    function_name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'function',
    }


class SchemaStep(ScraperStep):
    """
    Schema do deserialize the data.
    """

    __tablename__ = 'scraper_step_schema'

    id = Column(Integer, ForeignKey('scraper_step.id'), primary_key=True)

    schema_id = Column(Integer, ForeignKey('schema.id'))

    schema_object = relationship('Schema')

    __mapper_args__ = {
        'polymorphic_identity': 'schema',
    }
