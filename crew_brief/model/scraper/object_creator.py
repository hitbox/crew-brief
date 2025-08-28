from enum import IntEnum

import sqlalchemy as sa

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from crew_brief.model.base import Base
from crew_brief.model.mixin import NonEmptyStringMixin

class ObjectCreatorEnum(IntEnum):
    """
    Enumerate the object creators for Python-to-dabase link.
    """

    __model__ = 'ObjectCreator'

    LEG_IDENTIFIER = 1

    @property
    def callable(self):
        from crew_brief.model import LegIdentifier

        if self == ObjectCreatorEnum.LEG_IDENTIFIER:
            return LegIdentifier.from_data

    @property
    def description(self):
        if self is ObjectCreatorEnum.LEG_IDENTIFIER:
            return 'Create LegIdentifier object from deserialized data.'

    def get_instance(self, session):
        stmt = sa.select(ObjectCreator).where(ObjectCreator.id == self.value)
        return session.scalars(stmt).one()


class ObjectCreator(NonEmptyStringMixin, Base):
    """
    ObjectCreatorEnum mapped directly to database.
    """

    __tablename__ = 'object_creator'

    __enum__ = ObjectCreatorEnum

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    description = Column(String, nullable=False)

    @property
    def member(self):
        return self.__enum__(self.id)
