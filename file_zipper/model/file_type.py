import mimetypes

from functools import cached_property

import sqlalchemy.orm

from .base import Base
from .mixin import NameMixin

sa = sqlalchemy

class FileType(Base, NameMixin):
    """
    Describe what type of file a path points to.
    """
    # The motivation here is to avoid too much data on the Path objects.

    __tablename__ = 'filetype'

    __column_args__ = {
        'name': {
            'doc': 'Friendly name for file type.',
        },
    }

    __display_order__ = [
        'name',
        'mime_type',
    ]

    mime_type = sa.Column(
        sa.String,
        sa.CheckConstraint('length(mime_type) > 0'),
        nullable = False,
        unique = True,
    )

    path = sa.orm.relationship(
        'Path',
        back_populates = 'file_type',
        doc = 'The Path object this object describes.',
    )

    @classmethod
    def from_filename(cls, filename, session):
        mime_type, _ = mimetypes.guess_type(filename)
        stmt = sa.select(cls).filter(cls.mime_type == mime_type)
        return session.scalars(stmt).one()

    @cached_property
    def display_string(self):
        return self.name
