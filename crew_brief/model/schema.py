import importlib.util
import inspect
import re

from flask import send_file
from flask import url_for
from markupsafe import Markup
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from crew_brief.util import load_from_path

from .base import Base
from .mixin import CodePairMixin
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin
from .mixin import UniqueNameMixin

class Schema(Base, TimestampMixin, NonEmptyStringMixin, UniqueNameMixin):
    """
    Schema object.
    """

    human_description = 'Deserialize string data from filenames into Python types.'

    __tablename__ = 'schema'

    id = Column(Integer, primary_key=True)

    schema_import_path = Column(
        String,
        nullable = False,
        doc = 'Import path to schema class.',
    )

    def schema_class(self):
        """
        Get the schema class from import path.
        """
        return load_from_path(self.schema_import_path)
