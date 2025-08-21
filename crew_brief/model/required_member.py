from markupsafe import Markup
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

class RequiredMember(TimestampMixin, NonEmptyStringMixin, Base):
    """
    Zip file member requirement to qualify for completeness of zip.
    """

    human_description = 'Name of a member required to exist in a zip. These are grouped by ZipSpec objects.'

    __tablename__ = 'required_member'

    id = Column(Integer, primary_key=True)

    zip_spec_id = Column(Integer, ForeignKey('zip_spec.id'))

    zip_spec = relationship(
        'ZipSpec',
        back_populates = 'required_members',
    )

    filename = Column(
        String,
        nullable = False,
    )

    def __html__(self):
        return Markup(self.filename)
