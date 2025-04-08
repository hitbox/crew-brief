import os

import sqlalchemy as sa

from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base

class Path(Base):
    """
    Filesystem path.
    """

    __tablename__ = 'path'

    __display_order__ = [
        'name',
        'path',
    ]

    path = sa.Column(
        sa.String,
        unique = True,
        doc = 'Filesystem path.',
    )

    file_type_id = sa.Column(
        sa.ForeignKey('filetype.id'),
        nullable = False,
    )

    file_type = sa.orm.relationship(
        'FileType',
        back_populates = 'path',
        doc = 'Object describing what type of file this is.',
    )

    glob_id = sa.Column(
        sa.ForeignKey('glob.id'),
        nullable = True,
    )

    glob = sa.orm.relationship(
        'Glob',
        back_populates = 'paths',
        doc = 'The glob that produced this path.',
    )

    excluded_path = sa.orm.relationship(
        'ExcludedPath',
        back_populates = 'path',
        uselist = False,
    )

    data = sa.Column(
        sa.PickleType,
        nullable = True,
        doc = 'Data from path.',
    )

    @classmethod
    def from_glob(cls, path, globobj):
        """
        New Path object from path string and glob object.
        """
        return cls(path=path, glob=globobj)

    @property
    def basename(self):
        return os.path.basename(self.path)

    @property
    def display_string(self):
        return self.path
