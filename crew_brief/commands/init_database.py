import pickle

from crew_brief import configlib
from crew_brief import constants
from crew_brief.paths import walk_paths

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
