"""
Functions for the commands that the command-line interface reveals.
"""
import copy
import pickle

from pprint import pprint

try:
    import win32com.client as win32
except ImportError:
    win32 = None

from crew_brief import configlib
from crew_brief import constants
from crew_brief import databaselib
from crew_brief import discover
from crew_brief import nodes
from crew_brief import output
from crew_brief import rowifier
from crew_brief import schema
from crew_brief import shapers

def get_member_data(zip_path, member_re):
    """
    """
    with zipfile.ZipFile(zip_path) as _zipfile:
        for member in _zipfile.namelist():
            if member_re.match(member):
                member_file = _zipfile.open(member)
                member_json = member_file.read()
                member_data = json.loads(member_json)
                return member_data

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

def init_database(args):
    """
    Load a pickle database with data scraped from the paths and zip files.
    """
    config = configlib.from_args(args)

    logger = logging.getLogger('init_database')

    database_fn = config[constants.NAME]['database']

    # Load configuration.
    tops_and_regexes = list(configlib.get_tops_and_regexes(config))
    member_re = re.compile(config[constants.NAME]['member'])

    # Ensure database file exists.
    if not os.path.exists(database_fn):
        with open(database_fn, 'wb') as database_file:
            database = pickle.dump([], database_file)

    with open(database_fn, 'rb') as database_file:
        database = pickle.load(database_file)
        processed_paths = set(data['path'] for data in database)

    try:
        for top, path_data_regex in tops_and_regexes:
            for path in walk_paths(top):
                # Skip already processed.
                if path in processed_paths:
                    continue

                # Get data from path using a regex.
                path_match = path_data_regex.match(path)
                if not path_match:
                    raise ValueError('Path does not match regex.')
                path_data = path_match.groupdict()

                # Get data from zip file.
                try:
                    member_data = get_member_data(path, member_re)
                except:
                    logger.exception('An exception occurred.')
                else:
                    entry = dict(
                        path = path,
                        path_data = path_data,
                        member_data = member_data,
                    )
                    database.append(entry)

                    # Save file path as processed.
                    processed_paths.add(path)
    finally:
        with open(database_fn, 'wb') as database_file:
            pickle.dump(database, database_file)


def make_hashable(obj):
    """
    Convert an object into a hashable form to store in a set.
    """
    if isinstance(obj, dict):
        return frozenset((key, make_hashable(value)) for key, value in obj.items())
    elif isinstance(obj, list):
        return tuple(make_hashable(item) for item in obj)
    elif isinstance(obj, set):
        return frozenset(make_hashable(item) for item in obj)
    elif isinstance(obj, tuple):
        return tuple(make_hashable(item) for item in obj)
    else:
        # Assume it's already hashable
        return obj

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
    # XXX
    # - This is inconsistent. The --unique doesn't work like when it's off.
    config = configlib.from_args(args)
    database = databaselib.database_from_config(config)
    unique = set()
    for zip_data in database:
        if args.schema:
            # Load/typify one at a time for quick results.
            zip_data = schema.pickle_schema.load(zip_data)
        drill_data = nodes.try_drill(
            zip_data,
            args.keys,
            ignore_missing = args.ignore_missing,
        )
        if args.unique:
            unique.add(make_type(drill_data))
        else:
            pprint(drill_data)
    if args.unique:
        pprint(unique)

def normal_run(args):
    """
    Look for new files and process them.
    """
    # TODO
    print('normal_run')
    config = configlib.from_args(args)
    pprint(config)

def sample_output(args):
    """
    Produce a sample Excel output.
    """
    limit = args.number
    config = configlib.from_args(args)
    path_format = args.output.format
    autofit_with_excel = args.autofit_with_excel
    excel_converter = output.ExcelConverter()

    member_data_shaper = shapers.MemberDataShaper()

    database = databaselib.database_from_config(config)

    database = discover.get_interesting_files(database)
    if not database:
        raise ValueError('No interesting data found.')

    # TODO
    # - Move Excel stuff somewhere else.
    member_data_rowifier = rowifier.MemberDataRowifier()
    import openpyxl

    for count, original_zip_data in enumerate(database):
        if count == limit:
            break

        # Load/convert to types.
        typed_zip_data = schema.pickle_schema.load(original_zip_data)

        wb = openpyxl.Workbook()
        ws = wb.active

        member_data = typed_zip_data['member_data']
        if member_data is not None:

            shaped_member_data = copy.deepcopy(member_data)
            member_data_shaper(shaped_member_data)

            pairs = member_data_rowifier(
                shaped_member_data,
                original = member_data,
            )
            for row_type, row in pairs:
                ws.append(row)

        output_path = path_format(**typed_zip_data)
        wb.save(output_path)

def discover_structure(args):
    """
    Print the strucure of the data in the database.
    """
    # XXX
    # - This doesn't work well.
    # - type_structure is removed from nodes.
    config = configlib.from_args(args)
    database = databaselib.database_from_config(config)

    for zip_data in database:
        if args.schema:
            # Load/typify one at a time for quick results.
            zip_data = schema.pickle_schema.load(zip_data)

        data = nodes.try_drill(
            zip_data,
            args.keys,
            ignore_missing = args.ignore_missing,
        )
        structures = list(nodes.type_structure(data))
        pprint(structures)

def unique_event_details(args):
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
