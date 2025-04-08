import re

import sqlalchemy.orm

from .base import Base

sa = sqlalchemy

class Match(Base):
    """
    Match object from regex result.
    """

    __tablename__ = 'match'

    string = sa.Column(
        sa.String,
        nullable = False,
    )

    groupdict = sa.Column(
        sa.JSON,
        nullable = True,
    )

    start_position = sa.Column(
        sa.Integer,
        nullable = False,
    )

    end_position = sa.Column(
        sa.Integer,
        nullable = False,
    )

    def recreate_match(self, pattern):
        return re.match(pattern, self.string)
