"""
Functions for the commands that the command-line interface reveals.
"""
import copy
import pickle

from pprint import pprint

import openpyxl

from crew_brief import configlib
from crew_brief import constants
from crew_brief import databaselib
from crew_brief import nodes
from crew_brief import schema

from .look import look
from .sample_output import sample_output

def get_member_data(zip_path, member_re):
    """
    Return the JSON data of the first matching member of a zip.
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
        # Ensure that we save progress.
        with open(database_fn, 'wb') as database_file:
            pickle.dump(database, database_file)

def normal_run(args):
    """
    Look for new files and process them.
    """
    # TODO
    print('normal_run')
    config = configlib.from_args(args)
    pprint(config)

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
