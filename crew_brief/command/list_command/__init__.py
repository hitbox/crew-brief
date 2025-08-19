import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import configlib

from . import list_object
from . import reference
from . import stats

def add_parser(subparsers):
    """
    Add sub-command parser for list commands.
    """
    # Put list commands under list sub-command.
    list_parser = subparsers.add_parser(
        'list',
        help = 'Sub-commands for list operations.',
    )
    configlib.add_config_option(list_parser)
    list_subparsers = list_parser.add_subparsers()

    list_object.add_commands(list_subparsers)
    reference.add_parser(list_subparsers)

    # Add statistics sub-command
    stats.add_parser(list_subparsers)
