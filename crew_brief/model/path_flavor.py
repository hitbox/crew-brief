from enum import IntEnum

import ntpath
import os
import posixpath

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import NonEmptyStringMixin

class PathFlavorEnum(IntEnum):
    """
    Enumerate common path flavors with associated module for manipulating them.
    """

    __model__ = 'PathFlavor'

    auto = 1
    posix = 2
    nt = 3

    @property
    def module(self):
        if self is PathFlavorEnum.auto:
            return os.path
        elif self is PathFlavorEnum.posix:
            return posixpath
        elif self is PathFlavorEnum.nt:
            return ntpath

    def instance(self, session):
        return session.get(PathFlavor, ident=self.value)


class PathFlavor(NonEmptyStringMixin, Base):
    """
    Flavor of path separator.
    """

    __tablename__ = 'path_flavor'

    __enum__ = PathFlavorEnum

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    os_walks = relationship(
        'OSWalk',
        back_populates = 'path_flavor_object',
    )

    @property
    def member(self):
        """
        Return Python side backing enum member.
        """
        return self.__enum__(self.id)

    @property
    def module(self):
        return self.member.module
