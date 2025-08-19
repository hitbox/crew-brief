import importlib
import re

from functools import cached_property

from flask import url_for
from markupsafe import Markup
from markupsafe import escape
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from .base import Base
from .mixin import ByMixin
from .mixin import CodePairMixin
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin
from .mixin import UniqueNameMixin

class Regex(
    Base,
    NonEmptyStringMixin,
    TimestampMixin,
    UniqueNameMixin,
    ByMixin,
):
    """
    Regex pattern object.
    """

    human_description = 'Regular expression object with a unique name.'

    __tablename__ = 'regex'

    id = Column(Integer, primary_key=True)

    pattern = Column(
        String,
        nullable = False,
        doc = 'Regex pattern',
    )

    description = Column(
        Text,
    )

    scraper_id = Column(Integer, ForeignKey('scraper.id'))

    scraper = relationship(
        'Scraper',
        back_populates = 'regexes',
        foreign_keys = [scraper_id],
    )

    position = Column(
        Integer,
        nullable = False,
        default = 0,
        server_default = '0',
        doc = 'Integer ordering for Scraper.regexes relationship.',
    )

    @validates('pattern')
    def validates_regex(self, key, value):
        raise_for_regex(value)
        return value

    def compile_pattern(self):
        try:
            return re.compile(self.pattern)
        except re.error as e:
            raise ValueError(f'Failed to compile pattern: {self.pattern}') from e


def raise_for_regex(pattern):
    try:
        return re.compile(pattern)
    except re.error:
        raise ValueError(f'Pattern failed to compile: {pattern}')
