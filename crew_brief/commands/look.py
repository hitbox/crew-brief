from pprint import pprint

from crew_brief import configlib
from crew_brief import databaselib
from crew_brief import nodes
from crew_brief import schema

def make_type(obj):
    if isinstance(obj, dict):
        return frozenset((key, make_type(value)) for key, value in obj.items())
    elif isinstance(obj, list):
        return tuple(make_type(item) for item in obj)
    elif isinstance(obj, set):
        return frozenset(make_type(item) for item in obj)
    elif isinstance(obj, tuple):
        return tuple(make_type(item) for item in obj)
    else:
        return type(obj)

def look(args):
    """
    Print values from database.
    """
    config = configlib.from_args(args)
    database = databaselib.database_from_config(config)
    if args.unique:
        values = set()
        add_data = values.add
    else:
        values = list()
        add_data = values.append
    for zip_data in database:
        if args.schema:
            # Load/typify one at a time for quick results.
            zip_data = schema.pickle_schema.load(zip_data)
        drill_data = nodes.try_drill(
            zip_data,
            args.keys,
            ignore_missing = args.ignore_missing,
        )
        add_data(make_type(drill_data))
    pprint(values)


