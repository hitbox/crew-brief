import importlib
import os

from functools import cached_property

import sqlalchemy.orm

from sqlalchemy.ext.associationproxy import association_proxy

from file_zipper import parse

from .base import Base

sa = sqlalchemy

class PathMatch(Base):
    """
    Result of each PathParser iteration of paths and regexes.
    """

    __tablename__ = 'pathmatch'

    path_parser_id = sa.Column(
        sa.ForeignKey('pathparser.id'),
        nullable = False,
    )

    path_parser = sa.orm.relationship(
        'PathParser',
        back_populates = 'path_match',
    )

    path = sa.orm.relationship(
        'Path',
        back_populates = 'path_match',
        uselist = False,
    )

    data = sa.Column(
        sa.PickleType,
        nullable = False,
        doc = 'Data from path regex match object.',
    )

    @property
    def collapsed_data(self):
        return parse.collapse_dict(self.data)

    @cached_property
    def display_string(self):
        return self.path.path
