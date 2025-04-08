import re

from functools import cached_property

import sqlalchemy.orm

from .base import Base
from .mixin import NameMixin

sa = sqlalchemy

class Regex(Base, NameMixin):
    """
    A regex used to parse data from paths.
    """

    __tablename__ = 'regex'

    __column_args__ = {
        'name': {
            'doc':  'Friendly name for regular expression.',
        },
    }

    __display_order__ = [
        'name',
        'pattern_string',
        'flags',
        'path_parser',
    ]

    description = sa.Column(
        sa.String,
        sa.CheckConstraint('length(description) > 0'),
        nullable = True,
    )

    pattern_string = sa.Column(
        sa.String,
        nullable = False,
        doc = 'Regex pattern.',
    )

    flags = sa.Column(
        sa.Integer,
        default = 0,
        nullable = False,
        doc = 'Regular expression flags.',
    )

    glob_id = sa.Column(
        sa.ForeignKey('glob.id'),
        nullable = False,
    )

    glob = sa.orm.relationship(
        'Glob',
        back_populates = 'regexes',
        doc = 'The glob object used to produce paths'
              ' for this regex to match against.',
    )

    schema_id = sa.Column(
        sa.ForeignKey('schema.id'),
        nullable = False,
    )

    schema = sa.orm.relationship(
        'Schema',
        doc = 'Schema applied to match.groupdict().',
    )

    @sa.orm.validates('pattern_string')
    def validate_regex(self, key, value):
        """
        Validate regex compilation and that pattern has named capture groups.
        """
        compiled = re.compile(value)

        if not compiled.groupindex:
            raise ValueError('Regex must contain named capture groups.')

        return value

    @cached_property
    def compiled(self):
        """
        Compile regex pattern into re.Pattern.
        """
        return re.compile(self.pattern_string, self.flags)
