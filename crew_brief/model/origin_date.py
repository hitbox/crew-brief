import sqlalchemy as sa

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin
from .mixin import InstanceMixin

class OriginDate(Base, TimestampMixin, InstanceMixin):
    """
    Flight origin date object.
    """

    __tablename__ = 'origin_date'

    id = Column(Integer, primary_key=True)

    origin_date = Column(Date, nullable=False)

    leg_identifiers = relationship(
        'LegIdentifier',
        back_populates = 'origin_date_object',
    )

    @classmethod
    def creator(cls, origin_date):
        return cls(origin_date=origin_date)

    @classmethod
    def from_key_values(cls, origin_date):
        return cls(origin_date=origin_date)

    @classmethod
    def get_or_create_by_origin_date(cls, session, origin_date):
        instance = session.scalars(sa.select(cls).where(cls.origin_date == origin_date)).one_or_none()
        if instance is None:
            instance = cls(origin_date=origin_date)
            session.add(instance)
        return instance

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.origin_date < other.origin_date

    def __html__(self):
        return self.origin_date
