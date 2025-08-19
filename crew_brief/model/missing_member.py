from markupsafe import Markup
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

class MissingMember(Base, TimestampMixin, NonEmptyStringMixin):
    """
    Name inside a ZIP that is missing from the RequiredMember objects.
    """

    __tablename__ = 'missing_member'

    leg_file_id = Column(Integer, ForeignKey('leg_file.id'), primary_key=True)
    leg_file = relationship('LegFile', back_populates='missing_members')

    required_member_id = Column(Integer, ForeignKey('required_member.id'), primary_key=True)
    required_member = relationship('RequiredMember')

    required_filename = association_proxy('required_member', 'filename')

    def __eq__(self, other):
        from .required_member import RequiredMember
        if isinstance(other, RequiredMember):
            return other.filename == self.required_member.filename
        else:
            return super().__eq__(other)

    def __html__(self):
        return Markup(f'<pre class="data">{ self.required_filename }</pre>')
