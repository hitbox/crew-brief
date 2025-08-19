from operator import attrgetter
from operator import itemgetter

import sqlalchemy as sa

from crew_brief.model import LegFile
from crew_brief.model import LegIdentifier
from crew_brief.model import MimeType
from crew_brief.model import MissingMember
from crew_brief.model import OriginDate

from .completeness import select_complete_leg_files
from .completeness import select_complete_zip_count_for_year_by_month_day
from .completeness import select_complete_zip_since
from .completeness import select_incomplete_leg_files
from .completeness import select_yearly_complete_zip_count_by_date
from .constant import fields_for_unique_leg_identifier
from .constant import get_leg_identifier_unique_key_attrs
from .constant import get_leg_identifier_unique_key_items
from .duplicate import select_duplicate_leg_identifiers
from .group_by_leg_identifier import select_leg_identifiers_with_partial
from .parsing import select_parsed_files
from .parsing import select_unparsed_leg_files_for_walker

def select_missing_members_groups():
    """
    Select unique sets of MissingMember ids and the LegFile ids with a count.
    """
    mm = sa.orm.aliased(MissingMember)

    file_sets = (
        sa.select(
            mm.leg_file_id,
            sa.func.array_agg(
                mm.required_member_id,
                distinct = True,
                postgresql_order_by = mm.required_member_id,
            ).label('required_set'),
        )
        .group_by(mm.leg_file_id)
        .cte('file_sets')
    )

    grouped_stmt = (
        sa.select(
            file_sets.c.required_set,
            sa.func.array_agg(file_sets.c.leg_file_id).label('file_ids'),
            sa.func.cardinality(file_sets.c.required_set).label('set_size'),
        )
        .group_by(file_sets.c.required_set)
        .order_by(sa.func.cardinality(file_sets.c.required_set))
    )
    return grouped_stmt

def select_zip_files_missing_members(required_member_ids):
    mm = sa.orm.aliased(MissingMember)
    leg_file_ids_stmt = (
        sa.select(mm.leg_file_id)
        .group_by(mm.leg_file_id)
        .having(
            sa.func.array_agg(
                mm.required_member_id,
                distinct = True,
                postgresql_order_by = mm.required_member_id,
            ) == sa.cast(required_member_ids, sa.ARRAY(sa.Integer))
        )
    )
    return leg_file_ids_stmt

def null_join(col1, col2):
    # They are equal or both are null.
    return sa.or_(col1 == col2, sa.and_(col1.is_(None), col2.is_(None)))

def select_leg_files_for_walker(os_walk):
    stmt = (
        sa.select(LegFile)
        .where(
            # LegFile objects created by this OSWalk object
            LegFile.os_walk == os_walk,
        )
    )
    return stmt

def select_zip_files():
    """
    Select LegFile objects that are certainely ZIP files. They are
    zipfile.is_zipfile and mime detected as a ZIP.
    """
    stmt = (
        sa.select(LegFile)
        .join(MimeType)
        .where(
            # Is ZIP file
            LegFile.is_zipfile.is_(True),
            # MIME type looks like a ZIP
            MimeType.is_mime_zip.is_(True),
        )
    )
    return stmt

def select_unparsed_count_by_mime_and_is_zipfile():
    count = sa.func.count().label('count')
    stmt = sa.select(
        count,
        LegFile.is_zipfile,
        MimeType.mime,
    ).select_from(
        LegFile
    ).join(
        MimeType,
    ).where(
        LegFile.leg_identifier_id.is_(None),
    ).group_by(
        LegFile.is_zipfile,
        MimeType.mime,
    ).order_by(
        count.desc(),
    )
    return stmt

def select_files_for_unparsed_count_by_mime_and_is_zipfile(is_zipfile, mime):
    """
    Unparsed LegFile objects for is_zipfile and mime text.
    """
    stmt = sa.select(
        LegFile,
    ).join(
        MimeType,
    ).where(
        LegFile.leg_identifier_id.is_(None),
        LegFile.is_zipfile == is_zipfile,
        MimeType.mime == mime,
    )
    return stmt
