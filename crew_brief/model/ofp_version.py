import sqlalchemy as sa

from markupsafe import Markup
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from .base import Base
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

def check_constraint_null_or_nonnegative(column_name):
    return CheckConstraint(
        f'{column_name} IS NULL OR {column_name} >= 0',
        name = 'check_ofp_{column_name}_null_or_nonnegative',
    )

class OFPVersion(NonEmptyStringMixin, TimestampMixin, Base):
    """
    Operational Flight Plan Version
    """

    __tablename__ = 'ofp_version'

    __table_args__ = (
        UniqueConstraint('major', 'minor', 'patch'),
    )

    id = Column(Integer, primary_key=True)

    major = Column(
        Integer,
        check_constraint_null_or_nonnegative('major'),
        nullable = True,
    )

    minor = Column(
        Integer,
        check_constraint_null_or_nonnegative('minor'),
        nullable = True,
    )

    patch = Column(
        Integer,
        check_constraint_null_or_nonnegative('patch'),
        nullable = True,
    )

    leg_identifiers = relationship(
        'LegIdentifier',
        back_populates = 'ofp_version_object',
    )

    @hybrid_property
    def dotted_string(self):
        """
        OFPVersion components as a dot separated string.
        """
        return f'{self.major}.{self.minor}.{self.patch}'

    @dotted_string.expression
    def dotted_string(cls):
        return sa.func.concat(
            sa.func.cast(cls.major, String),
            '.',
            sa.func.cast(cls.minor, String),
            '.',
            sa.func.cast(cls.patch, String),
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
