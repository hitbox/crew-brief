from enum import IntEnum

import sqlalchemy as sa

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from crew_brief.model.base import Base
from crew_brief.model.mixin import NonEmptyStringMixin

class ScraperStepTypeEnum(IntEnum):
    """
    Polymorphic identity of a ScraperStep subclass. Values are used to enforce
    the relative ordering of the steps.
    """

    __model__ = 'ScraperStepType'

    # Parse filename.
    REGEX = 1

    # Optional, more parsing.
    FUNCTION = 2

    # Deserialize scraped data.
    SCHEMA = 3

    # Create and object from deserialized data.
    OBJECT = 4

    # Parent Scraper class uses this to enforce required steps.
    __required__ = (REGEX, SCHEMA, OBJECT)

    @property
    def description(self):
        if self is ScraperStepTypeEnum.REGEX:
            return 'Capture group regex to scrape path.'
        elif self is ScraperStepTypeEnum.FUNCTION:
            return (
                'Callable that updates the result'
                ' of groupdict from the REGEX step.'
            )
        elif self is ScraperStepTypeEnum.SCHEMA:
            return (
                'Schema object with .load method to deserialize scraped data.'
            )
        elif self is ScraperStepTypeEnum.OBJECT:
            return 'Step to create object from deserialized data.'

    def get_instance(self, session):
        model = eval(self.__model__)
        stmt = sa.select(model).where(model.id == self)
        return session.scalars(stmt).one()


class ScraperStepType(Base):
    """
    Type of ScraperStep backed by enum.
    """

    __tablename__ = 'scraper_step_type'

    __enum__ = ScraperStepTypeEnum

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    description = Column(String, nullable=False)

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
    Base polymorphic class for scraper steps.
    """

    __tablename__ = 'scraper_step'

    id = Column(Integer, primary_key=True)

    scraper_id = Column(ForeignKey('scraper.id'))

    scraper = relationship(
        'Scraper',
        back_populates = '_steps',
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

    def __html__(self):
        return self.regex.name


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

    def __html__(self):
        return self.function_name


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

    def __html__(self):
        return self.schema_object.name


class ObjectStep(ScraperStep):
    """
    ScraperStep database object to deserialized data to object.
    """

    __tablename__ = 'scraper_step_object'

    __mapper_args__ = {
        'polymorphic_identity': ScraperStepTypeEnum.OBJECT,
    }

    id = Column(
        Integer,
        ForeignKey('scraper_step.id'),
        primary_key = True,
    )

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

    def __html__(self):
        # XXX:
        # - Ok, these __html__ things work but it feels off.
        return self.creator_object.name
