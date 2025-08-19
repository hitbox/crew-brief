import sqlalchemy as sa

from crew_brief.model import LegFile
from crew_brief.model import LegIdentifier

def select_leg_identifiers_with_partial():
    """
    Group files by leg identifier.
    """
    # Step 1: build a file-level grouping
    file_group = (
        sa.select(
            LegIdentifier.airline_id,
            LegIdentifier.origin_date_id,
            LegIdentifier.flight_number_id,
            LegIdentifier.departure_airport_id,
            LegIdentifier.destination_airport_id,
            LegIdentifier.ofp_version,
            sa.func.count(LegFile.id).label('file_count'),
            sa.func.sum(sa.case((LegFile.is_zipfile.is_(True), 1), else_=0)).label('zip_count'),
            sa.func.sum(sa.case((LegFile.is_zipfile.is_(False), 1), else_=0)).label('not_zip_count'),
        )
        .join(LegFile)
        .group_by(
            LegIdentifier.airline_id,
            LegIdentifier.origin_date_id,
            LegIdentifier.flight_number_id,
            LegIdentifier.departure_airport_id,
            LegIdentifier.destination_airport_id,
            LegIdentifier.ofp_version,
        )
        .cte('file_group')
    )

    # Step 2: filter file groups
    subq = (
        sa.select(
            file_group.c.airline_id,
            file_group.c.origin_date_id,
            file_group.c.flight_number_id,
            file_group.c.departure_airport_id,
            file_group.c.destination_airport_id,
            file_group.c.ofp_version,
        )
        .where(
            # More than one file.
            file_group.c.file_count > 1,
            # At least one zip file.
            file_group.c.zip_count > 0,
            # At least one non-zip file.
            file_group.c.not_zip_count > 0,
        )
        .subquery()
    )

    # Step 3: join back to leg_identifier
    stmt = (
        sa.select(LegIdentifier)
        .join(
            subq,
            sa.and_(
                LegIdentifier.airline_id == subq.c.airline_id,
                LegIdentifier.origin_date_id == subq.c.origin_date_id,
                LegIdentifier.flight_number_id == subq.c.flight_number_id,
                LegIdentifier.departure_airport_id == subq.c.departure_airport_id,
                LegIdentifier.destination_airport_id == subq.c.destination_airport_id,
                sa.or_(
                    LegIdentifier.ofp_version == subq.c.ofp_version,
                    sa.and_(
                        LegIdentifier.ofp_version == None,
                        subq.c.ofp_version == None,
                    ),
                )
            )
        )
    )
    return stmt
