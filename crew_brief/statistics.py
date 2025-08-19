import sqlalchemy as sa

from crew_brief.model import LegFile
from crew_brief.model import LegIdentifier
from crew_brief.model import MimeType

def file_stats(session):
    stats = {}

    count_field = sa.func.count()
    is_really_zip = sa.and_(
        MimeType.is_mime_zip,
        LegFile.is_zipfile,
    )
    stmt = (
        sa.select(
            MimeType.mime,
            is_really_zip.label('is_really_zip'),
            count_field,
        )
        .select_from(LegFile)
        .join(MimeType)
        .outerjoin(LegIdentifier)
        .group_by(
            MimeType.mime,
            is_really_zip,
        )
        .order_by(
            count_field.desc(),
        )
    )
    stats['by_type_and_zip'] = session.execute(stmt).mappings().all()

    stats['total_files'] = session.scalar(sa.select(sa.func.count()).select_from(LegFile))

    stats['unparsed_count'] = session.scalar(
        sa.select(sa.func.count())
        .select_from(LegFile)
        .where(LegFile.leg_identifier_id == None)
    )

    return stats
