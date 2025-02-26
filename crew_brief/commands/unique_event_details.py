from pprint import pprint

from crew_brief import configlib
from crew_brief import databaselib
from crew_brief import schema

def unique_event_details(args):
    """
    Pretty print unique eventDetails from configured database.
    """
    config = configlib.from_args(args)
    database = databaselib.database_from_config(config)
    structures = set()
    for zip_data in database:
        if args.schema:
            # Load/typify one at a time for quick results.
            zip_data = schema.pickle_schema.load(zip_data)
        member_data = zip_data['member_data']
        if member_data:
            user_events = member_data['userEvents']
            for user_event in user_events:
                event_details = user_event.get('eventDetails')
                if event_details:
                    # Add keys.
                    structures.add(tuple(event_details))
    pprint(structures)
