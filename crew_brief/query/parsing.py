import sqlalchemy as sa

from crew_brief.model import LegFile
from crew_brief.model import LegIdentifier
from crew_brief.model import OriginDate

def select_unparsed_leg_files_for_walker(os_walk):
    stmt = (
        sa.select(LegFile)
        .where(
            sa.or_(
                LegFile.force_parse.is_(True),
                sa.and_(
                    # Unparsed: not already associated with a LegIdentifier object.
                    LegFile.leg_identifier_id.is_(None),
                    # Not indicated an exception for parsing
                    LegFile.parse_exception_at.is_(None),
                    # LegFile objects created by this OSWalk object
                    LegFile.os_walk == os_walk,
                ),
            ),
        )
    )
    return stmt

def select_parsed_files(model, is_zipfile=None):
    stmt = (
        sa.select(LegFile)
        .join(LegIdentifier)
        .join(OriginDate)
        .where(
            LegFile.leg_identifier_id != None,
        )
        .order_by(
            OriginDate.origin_date.desc(),
        )
    )
    if is_zipfile is not None:
        stmt = stmt.where(LegFile.is_zipfile == is_zipfile)
    return stmt
