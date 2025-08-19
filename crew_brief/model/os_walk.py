import os

import sqlalchemy

from markupsafe import Markup
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import ByMixin
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin
from .mixin import UniqueNameMixin
from .path_flavor import PathFlavor

class OSWalk(
    Base,
    ByMixin,
    NonEmptyStringMixin,
    TimestampMixin,
    UniqueNameMixin,
):
    """
    os.walk arguments.
    """

    __tablename__ = 'os_walk'

    human_description = 'Recursively walk a directory for file paths.'

    id = Column(Integer, primary_key=True)

    top = Column(
        String,
        nullable = False,
        doc = 'Top directory to start walking recursively.',
    )

    topdown = Column(
        Boolean,
        nullable = False,
        server_default = 'true',
        doc = 'Top-down traversal if true, bottom-up otherwise.',
    )

    # TODO: onerror argument for os.walk

    followlinks = Column(
        Boolean,
        nullable = False,
        server_default = 'false',
        doc = 'Follow symbolic links.',
    )

    path_flavor = Column(
        sqlalchemy.Enum(PathFlavor, name='path_flavor_enum'),
        nullable = False,
        server_default = PathFlavor.auto.value,
        doc = 'Flavor of path separators.',
    )

    leg_files = relationship(
        'LegFile',
        back_populates = 'os_walk',
    )

    @property
    def normalized_top(self):
        return self.path_flavor.normpath(self.top)

    def walk_filenames(self, onerror=None, **kwargs):
        """
        Recursively generate full path filenames of file from top.
        """
        # Default kwargs from this instance, if not given.
        kwargs.setdefault('topdown', self.topdown)
        kwargs.setdefault('followlinks', self.followlinks)
        if onerror is not None:
            kwargs.setdefault('onerror', onerror)

        # XXX
        # os.walk renders path_flavor somewhat useless, but if future walkers
        # are needed this can be factored into something else that abstracts
        # walking other systems.
        for dirpath, dirnames, filenames in os.walk(self.top, **kwargs):
            for filename in filenames:
                path = self.path_flavor.join(dirpath, filename)
                yield self.path_flavor.normpath(path)

    def relative_to_top(self, path):
        """
        Return path as relative to this top path.
        """
        return self.path_flavor.relpath(path, self.top)

    def describe_short(self):
        """
        Short description string.
        """
        return f'{self.name} {self.normalized_top}'

    def __html__(self):
        return Markup(self.name)
