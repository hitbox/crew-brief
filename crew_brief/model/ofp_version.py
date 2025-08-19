from markupsafe import Markup
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy import select
from sqlalchemy.orm import validates

from .base import Base
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

class OFPVersion(Base, TimestampMixin, NonEmptyStringMixin):
    """
    Operational Flight Plan Version
    """

    __tablename__ = 'ofp_version'

    id = Column(Integer, primary_key=True)

    major = Column(Integer, nullable=True)
    minor = Column(Integer, nullable=True)
    patch = Column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint('major', 'minor', 'patch'),
        CheckConstraint('major IS NULL OR major >= 0', name='check_ofp_major_null_or_nonnegative'),
        CheckConstraint('minor IS NULL OR minor >= 0', name='check_ofp_minor_null_or_nonnegative'),
        CheckConstraint('patch IS NULL OR patch >= 0', name='check_ofp_patch_null_or_nonnegative'),
    )

    @validates('major', 'minor', 'patch')
    def validate_nonnegative(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f'{key} must be non-negative')
        return value

    @classmethod
    def get_or_create_by_integers(cls, session, major, minor, patch):
        stmt = select(cls).where(cls.major == major, cls.minor == minor, cls.patch == patch)
        instance = session.scalars(stmt).one_or_none()
        if instance is None:
            instance = cls(major=major, minor=minor, patch=patch)
            session.add(instance)
        return instance

    @classmethod
    def get_or_create_by_dict(cls, session, data):
        return cls.get_or_create_by_integers(session, data['major'], data['minor'], data['patch'])

    def __html__(self):
        return Markup(f'<span>{self.major}.{self.minor}.{self.patch}</span>')
