from crew_brief import configlib

from . import init
from . import seed

def add_parser(subparsers):
    """
    Add sub-command parser for database.
    """
    # Put database commands under database sub-command.
    database_parser = subparsers.add_parser(
        'database',
        help = 'Sub-commands for database operations.',
    )
    configlib.add_config_option(database_parser)
    database_subparsers = database_parser.add_subparsers()

    init.add_parser(database_subparsers)
    seed.add_parser(database_subparsers)
