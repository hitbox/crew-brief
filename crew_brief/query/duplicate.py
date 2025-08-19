import sqlalchemy as sa

from crew_brief.model import LegIdentifier

from .constant import fields_for_unique_leg_identifier

def select_duplicate_leg_identifiers():
    dupe_subquery = (
        sa.select(*fields_for_unique_leg_identifier)
        .group_by(*fields_for_unique_leg_identifier)
        .having(sa.func.count() > 1)
        .subquery()
    )

    dupe_leg_identifiers_query = (
        sa.select(LegIdentifier)
        .join(
            dupe_subquery,
            sa.and_(
                LegIdentifier.airline_id == dupe_subquery.c.airline_id,
                LegIdentifier.flight_number_id == dupe_subquery.c.flight_number_id,
                LegIdentifier.origin_date_id == dupe_subquery.c.origin_date_id,
                LegIdentifier.departure_airport_id == dupe_subquery.c.departure_airport_id,
                LegIdentifier.destination_airport_id == dupe_subquery.c.destination_airport_id,
                null_join(LegIdentifier.ofp_version, dupe_subquery.c.ofp_version),
                null_join(LegIdentifier.datetime, dupe_subquery.c.datetime),
            ),
        )
    )

    return dupe_leg_identifiers_query
