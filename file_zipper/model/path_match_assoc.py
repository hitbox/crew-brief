import sqlalchemy.orm

from .base import Base

sa = sqlalchemy

class PathMatchAssoc(Base):
    """
    """

    __tablename__ = 'path_match_assoc'

    path_id = sa.Column(
        sa.ForeignKey('path.id'),
        primary_key = True,
    )

    path = sa.orm.relationship('Path')

    path_match_id = sa.Column(
        sa.ForeignKey('pathmatch.id'),
        nullable = True,
    )

    path_match = sa.orm.relationship(
        'PathMatch',
        foreign_keys = [path_match_id],
    )
