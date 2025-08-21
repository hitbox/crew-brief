from operator import attrgetter
from operator import itemgetter

from crew_brief.model import LegIdentifier

fields_for_unique_leg_identifier = (
    LegIdentifier.airline_id,
    LegIdentifier.flight_number_id,
    LegIdentifier.origin_date_id,
    LegIdentifier.departure_airport_id,
    LegIdentifier.destination_airport_id,
    LegIdentifier.ofp_version_id,
    LegIdentifier.datetime,
)

keys_for_unique_leg_identifier = tuple(attr.name for attr in fields_for_unique_leg_identifier)
get_leg_identifier_unique_key_attrs = attrgetter(*keys_for_unique_leg_identifier)
get_leg_identifier_unique_key_items = itemgetter(*keys_for_unique_leg_identifier)
