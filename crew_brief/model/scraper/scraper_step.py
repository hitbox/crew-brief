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
    """
    Type of scraper step. Values are used to enforce the relative ordering of
    the steps.
    """

    # Parse filename.
    REGEX = 1

    # Optional, more parsing.
    FUNCTION = 2

    # Deserialize scraped data.
    SCHEMA = 3

    # Create and object from deserialized data.
    OBJECT = 4

    __required__ = (REGEX, SCHEMA, OBJECT)


class ScraperStepType(Base):
    """
    Type of ScraperStep backed by enum.
    """

    __tablename__ = 'scraper_step_type'

    __enum__ = ScraperStepTypeEnum

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    @classmethod
    def instances_from_enum(cls):
        return [cls(id=member.value, name=member.name) for member in cls.__enum__]

    @property
    def member(self):
        return self.__enum__(self.id)

    def __eq__(self, other):
        if isinstance(other, ScraperStepTypeEnum):
            return self.id == other.value
        return super().__eq__(other)


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
        'polymorphic_identity': None,
    }


class RegexStep(ScraperStep):
    """
    LegFile path capture group regex parser.
    """

    __tablename__ = 'scraper_step_regex'

    __mapper_args__ = {
        'polymorphic_identity': ScraperStepTypeEnum.REGEX,
    }

    id = Column(Integer, ForeignKey('scraper_step.id'), primary_key=True)

    regex_id = Column(ForeignKey('regex.id'))

    regex = relationship('Regex')


class FunctionStep(ScraperStep):
    """
    Callable that adds more data to the group dict from the regex step.
    """

    __tablename__ = 'scraper_step_function'

    __mapper_args__ = {
        'polymorphic_identity': ScraperStepTypeEnum.FUNCTION,
    }

    id = Column(Integer, ForeignKey('scraper_step.id'), primary_key=True)

    function_name = Column(String)


class SchemaStep(ScraperStep):
    """
    Schema do deserialize the data.
    """

    __tablename__ = 'scraper_step_schema'

    __mapper_args__ = {
        'polymorphic_identity': ScraperStepTypeEnum.SCHEMA,
    }

    id = Column(Integer, ForeignKey('scraper_step.id'), primary_key=True)

    schema_id = Column(Integer, ForeignKey('schema.id'))

    schema_object = relationship('Schema')


class ObjectCreatorEnum(IntEnum):
    """
    Enumerate the object creators for Python-to-dabase link.
    """

    LEG_IDENTIFIER = 1

    @property
    def callable(self):
        from crew_brief.model import LegIdentifier

        if self == ObjectCreatorEnum.LEG_IDENTIFIER:
            return LegIdentifier.from_data


class ObjectCreator(NonEmptyStringMixin, Base):
    """
    ObjectCreatorEnum mapped directly to database.
    """

    __tablename__ = 'object_creator'

    __enum__ = ObjectCreatorEnum

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    @property
    def member(self):
        return self.__enum__(self.id)


class ObjectStep(ScraperStep):
    """
    ScraperStep database object to deserialized data to object.
    """

    __tablename__ = 'scraper_step_object'

    __mapper_args__ = {
        'polymorphic_identity': ScraperStepTypeEnum.OBJECT,
    }

    id = Column(Integer, ForeignKey('scraper_step.id'), primary_key=True)

    creator_id = Column(
        Integer,
        ForeignKey('object_creator.id'),
        nullable = False,
    )

    creator_object = relationship(
        'ObjectCreator',
    )

    @property
    def object_creator(self):
        """
        Callable to create database object.
        """
        return self.creator_object.member.callable
