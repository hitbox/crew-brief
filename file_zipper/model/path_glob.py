import sqlalchemy.orm

from .base import Base

sa = sqlalchemy

class PathGlob(Base):
    """
    Associate exactly one Path object with the Glob object that produced it.
    The reason this exists is to allow stand alone Path objects.
    """

    __tablename__ = 'path_glob'

    path_id = sa.Column(
        sa.ForeignKey('path.id'),
        unique = True,
    )

    path = sa.orm.relationship('Path')

    glob_id = sa.Column(
        sa.ForeignKey('glob.id'),
        nullable = False,
    )

    glob = sa.orm.relationship('Glob')
