from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import ByMixin
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin
from .mixin import UniqueNameMixin

class ZipSpec(
    ByMixin,
    NonEmptyStringMixin,
    TimestampMixin,
    UniqueNameMixin,
    Base,
):
    """
    Group of named members required for a complete zip file.
    """

    human_description = 'Group of required member objects that satisfy a complete zip check.'

    __tablename__ = 'zip_spec'

    id = Column(Integer, primary_key=True)

    name = Column(
        String,
        nullable = False,
        unique = True,
        doc = 'Short unique name to get instances.',
    )

    description = Column(
        Text,
        doc = 'Describe why this ZIP specification exists.',
    )

    required_members = relationship(
        'RequiredMember',
        back_populates = 'zip_spec',
        cascade = 'all, delete-orphan',
    )
