import datetime
import os
import zipfile

import sqlalchemy as sa

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from crew_brief.util import hybrid_date_part
from crew_brief.util import url_for_instance
from htmlkit import unordered_list

from .base import Base
from .mixin import NonEmptyStringMixin
from .mixin import TimestampMixin

class LegFile(TimestampMixin, NonEmptyStringMixin, Base):
    """
    A file path with metadata about crew brief related processes.
    """

    human_description = 'Files indexed for matching against others.'

    __tablename__ = 'leg_file'

    id = Column(Integer, primary_key=True)

    path = Column(
        String,
        nullable = False,
        unique = True,
    )

    mtime = Column(
        Float,
        doc = 'Last observed modified time of file.',
    )

    os_walk_id = Column(
        Integer,
        ForeignKey('os_walk.id'),
    )

    os_walk = relationship(
        'OSWalk',
        back_populates = 'leg_files',
        doc = 'Object that produced the path.',
    )

    leg_identifier_id = Column(
        Integer,
        ForeignKey('leg_identifier.id'),
        nullable = True,
    )

    leg_identifier = relationship(
        'LegIdentifier',
        back_populates = 'leg_file',
        uselist = False,
    )

    missing_members = relationship(
        'MissingMember',
        back_populates = 'leg_file',
        cascade = 'all, delete-orphan',
        doc = 'Required member names missing from zip file.',
    )

    check_complete_at = Column(
        DateTime,
        nullable = True,
        server_default = None,
        doc = 'Timestamp for when check for zip completeness was last done.',
    )

    complete_at = Column(
        DateTime,
        nullable = True,
        server_default = None,
        doc = 'Timestamp when zip file was marked as complete.',
    )

    complete_at_year = hybrid_date_part('complete_at', 'year')
    complete_at_month = hybrid_date_part('complete_at', 'month')
    complete_at_day = hybrid_date_part('complete_at', 'day')

    @hybrid_property
    def complete_at_date(self):
        if self.complete_at is None:
            return None
        return self.complete_at.date

    @complete_at_date.expression
    def complete_at_date(cls):
        return sa.func.date(cls.complete_at)

    is_zipfile = Column(
        Boolean,
        nullable = False,
        default = False,
        server_default = sa.text('false'),
    )

    mime_type_id = Column(
        Integer,
        ForeignKey('mime_type.id'),
        nullable = False,
    )

    mime_type = relationship(
        'MimeType',
    )

    mime_type_is_mime_zip = association_proxy('mime_type', 'is_mime_zip')

    parse_regex_id = Column(
        Integer,
        ForeignKey('regex.id'),
        nullable = True,
        doc = 'Regex used to parse this file.',
    )

    parse_regex = relationship(
        'Regex',
    )

    parse_exception_at = Column(
        DateTime,
        nullable = True,
        doc = 'Timestamp of exception while parsing with regex.',
    )

    not_exists_at = Column(
        DateTime,
        nullable = True,
        doc = 'Timestamp file was observed not existing.',
    )

    force_parse = Column(
        Boolean,
        nullable = False,
        default = False,
        server_default = sa.text('false'),
        doc = 'Force parsing for file.',
    )

    file_operation_associations = relationship(
        'FileOperationAssociation',
        back_populates = 'leg_file',
    )

    @hybrid_property
    def is_really_zip(self):
        return self.is_zipfile and self.mime_type.is_mime_zip

    @is_really_zip.expression
    def is_really_zip(cls):
        from .mime_type import MimeType
        return sa.and_(
            cls.is_zipfile,
            MimeType.is_mime_zip,
        )

    @property
    def modified_at(self):
        return datetime.datetime.fromtimestamp(self.mtime)

    @property
    def path_relative_to_top(self):
        return self.os_walk.relative_to_top(self.path)

    @property
    def missing_members_ids_set(self):
        return frozenset((m.leg_file_id, m.required_member_id) for m in self.missing_members)

    @property
    def missing_members_names_set(self):
        return frozenset(m.required_member.filename for m in self.missing_members)

    def path_relative_to(self, path):
        return os.path.relative_to(self.path)

    def __html__(self):
        return self.path
