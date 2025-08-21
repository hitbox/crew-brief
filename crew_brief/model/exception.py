import traceback

import sqlalchemy as sa

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

class ExceptionType(NonEmptyStringMixin, Base):

    __tablename__ = 'exception_type'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    exceptions = relationship(
        'ExceptionInstance',
        back_populates = 'exception_type',
    )

    @classmethod
    def get_by_name(cls, session, name):
        return session.scalars(sa.select(cls).where(cls.name == name)).one_or_none()


class ExceptionInstance(NonEmptyStringMixin, Base):

    __tablename__ = 'exception_instance'

    id = Column(Integer, primary_key=True)

    exception_type_id = Column(
        Integer,
        ForeignKey('exception_type.id'),
        nullable = False,
    )

    exception_type = relationship(
        'ExceptionType',
        back_populates = 'exceptions',
    )

    message = Column(String, nullable=False)

    traceback = Column(String, nullable=False)

    @classmethod
    def from_exc(cls, session, exc):
        exc_type_name = type(exc).__name__
        exc_type = ExceptionType.get_by_name(session, exc_type_name)
        if not exc_type:
            exc_type = ExceptionType(name=exc_type_name)
            session.add(exc_type)

        instance = cls(
            exception_type = exc_type,
            message = str(exc),
            traceback = traceback.format_exc(),
        )
        session.add(instance)

        return instance
