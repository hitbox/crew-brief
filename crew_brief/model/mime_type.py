from markupsafe import Markup
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base
from .mixin import NonEmptyStringMixin

class MimeType(Base, NonEmptyStringMixin):
    """
    Table of mimetypes possible results.
    """

    __tablename__ = 'mime_type'

    id = Column(Integer, primary_key=True)

    mime = Column(String, nullable=False, unique=True)

    is_mime_zip = Column(Boolean, nullable=False)

    def __html__(self):
        return Markup(f'<pre>{self.mime}</pre>')
