import glob
import os

from functools import cached_property

import sqlalchemy.orm

from .base import Base
from .mixin import NameMixin

sa = sqlalchemy

class Glob(Base, NameMixin):
    """
    Arguments to glob.glob and glob.iglob.
    """

    __tablename__ = 'glob'

    __column_args__ = {
        'name': {
            'doc': 'Friendly name for glob pattern arguments.',
        },
    }

    __display_order__ = [
        'name',
        'root_dir',
        'pathname',
        'recursive',
    ]

    pathname = sa.Column(
        sa.String,
        sa.CheckConstraint('length(pathname) > 0'),
        nullable = False,
        doc = 'Path with optional magic glob elements.',
    )

    recursive = sa.Column(
        sa.Boolean,
        default = True,
        nullable = False,
        doc = 'Respect recursive ** magic.',
    )

    root_dir = sa.Column(
        sa.String,
        sa.CheckConstraint('length(root_dir) > 0'),
        doc = 'Root directory for searching.',
    )

    regexes = sa.orm.relationship(
        'Regex',
        doc = 'List of regexes to apply to each path until one matches.',
    )

    paths = sa.orm.relationship(
        'Path',
        back_populates = 'glob',
        doc = 'Paths produced by this glob.',
    )

    @cached_property
    def full_pathname(self):
        pathname = self.pathname
        if self.root_dir:
            pathname = os.path.join(self.root_dir, pathname)
        return os.path.normpath(pathname)

    def iglob(self, **kwargs):
        """
        Generate paths from self.
        """
        kwargs.setdefault('pathname', self.pathname)
        kwargs.setdefault('recursive', self.recursive)
        kwargs.setdefault('root_dir', self.root_dir)
        for filename in glob.iglob(**kwargs):
            if self.root_dir:
                filename = os.path.join(self.root_dir, filename)
            yield os.path.normpath(filename)
