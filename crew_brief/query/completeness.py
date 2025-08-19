import sqlalchemy as sa

from crew_brief.model import LegFile
from crew_brief.model import MimeType

def select_complete_leg_files():
    stmt = (
        sa.select(LegFile)
        .join(MimeType)
        .where(
            LegFile.is_really_zip.is_(True),
            # And marked complete
            LegFile.complete_at.is_not(None),
        )
    )
    return stmt

def select_incomplete_leg_files():
    stmt = (
        sa.select(LegFile)
        .join(MimeType)
        .where(
            # File not marked missing
            LegFile.not_exists_at.is_(None),
            # Is ZIP file
            LegFile.is_zipfile.is_(True),
            # Not marked completed yet.
            LegFile.complete_at.is_(None),
            # MIME type looks like a ZIP
            MimeType.is_mime_zip.is_(True),
        )
    )
    return stmt

def select_complete_zip_since(since_datetime):
    stmt = (
        sa.select(LegFile)
        .join(MimeType)
        .where(
            LegFile.is_zipfile.is_(True),
            MimeType.is_mime_zip.is_(True),
            LegFile.complete_at >= since_datetime,
        )
    )
    return stmt

def select_complete_zip_count_for_year_by_month_day(year):
    stmt = (
        sa.select(
            LegFile.complete_at_month.label('year'),
            LegFile.complete_at_month.label('month'),
            LegFile.complete_at_day.label('day'),
            sa.func.count(),
        )
        .where(
            LegFile.complete_at.isnot(None),
            LegFile.complete_at_year == year,
            LegFile.is_really_zip.is_(True),
        )
        .group_by(
            LegFile.complete_at_year,
            LegFile.complete_at_month,
            LegFile.complete_at_day,
        )
    )
    return stmt

def select_yearly_complete_zip_count_by_date(year):
    stmt = (
        sa.select(
            LegFile.complete_at_date,
            sa.func.count(),
        )
        .where(
            LegFile.complete_at.isnot(None),
            LegFile.complete_at_year == year,
            LegFile.is_really_zip.is_(True),
        )
        .group_by(
            LegFile.complete_at_date,
        )
    )
    return stmt
