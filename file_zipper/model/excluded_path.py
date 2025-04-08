from functools import cached_property

import sqlalchemy.orm

sa = sqlalchemy

from .base import Base

class ExcludedPath(Base):
    """
    Path object excluded from regex matching with a descriptive reason.
    """
    # The motivation here is to avoid too much data on Path objects.

    __tablename__ = 'excluded_paths'

    path_id = sa.Column(
        sa.ForeignKey('path.id'),
        nullable = False,
    )

    path = sa.orm.relationship(
        'Path',
        back_populates = 'excluded_path',
    )

    reason = sa.Column(
        sa.String,
        sa.CheckConstraint('length(reason) > 0'),
        nullable = False,
        doc = 'Reason for excluding this path from regex'
              ' matching and further processing.',
    )

    @cached_property
    def display_string(self):
        return self.path.path

    @classmethod
    def display_header(cls):
        return ['Path', 'Reason']
