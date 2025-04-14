import re

import openpyxl

from pprint import pprint

from crew_brief import configlib
from crew_brief import databaselib
from crew_brief import nodes
from crew_brief import schema

def add_parser(subparsers):
    """
    Add parser for look command.
    """
    look_parser = subparsers.add_parser('look')

    subcommands = look_parser.add_subparsers()

    look_parser = subcommands.add_parser(
        'database',
        help = database.__doc__,
    )
    look_parser.add_argument(
        '--unique',
        action = 'store_true',
        help = 'Print only unique values.',
    )
    look_parser.set_defaults(func=database)

    # find values in Excel files.
    find_parser = subcommands.add_parser(
        'find',
        help = find.__doc__,
    )
    find_parser.add_argument('files', nargs='+')
    find_parser.add_argument('-e', action='append')
    find_parser.set_defaults(func=find)

    values_parser = subcommands.add_parser(
        'values',
        help = values.__doc__,
    )
    values_parser.add_argument('config')
    values_parser.set_defaults(func=values)

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

def database(args):
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
    pickle_schema = schema.PickleSchema()
    for zip_data in database:
        if args.schema:
            # Load/typify one at a time for quick results.
            zip_data = pickle_schema.load(zip_data)
        drill_data = nodes.try_drill(
            zip_data,
            args.keys,
            ignore_missing = args.ignore_missing,
        )
        add_data(make_type(drill_data))
    pprint(values)

def find(args):
    """
    Grep for Excel files.
    """
    regexes = list(map(re.compile, args.e))

    for fn in args.files:
        wb = openpyxl.load_workbook(fn)
        for ws in wb:
            for row in ws:
                for cell in row:
                    if any(regex.search(str(cell.value)) for regex in regexes):
                        print((fn, cell.value))

def values(args):
    """
    Pretty print values from source files.
    """
    config = configlib.pyfile_config(args.config)

    try:
        for process in config.PROCESSES:
            for path_data in process._generate_paths({}):
                data = process.schema.load(path_data.data)
                pprint((path_data.path, data))
    except KeyboardInterrupt:
        pass
