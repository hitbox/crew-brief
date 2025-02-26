from crew_brief import configlib
from crew_brief import databaselib
from crew_brief import schema

def check_database(args):
    """
    Check assumptions against pickle database.
    """
    config = configlib.from_args(args)
    database = databaselib.database_from_config(config)
    typed_database = schema.pickle_schema.load(
        database,
        many = True,
    )

    for zip_data in typed_database:
        member_data = zip_data.get('member_data')
        assert isinstance(user_event['eventDetails'], dict)
