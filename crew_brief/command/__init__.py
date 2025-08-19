"""
Functions for the commands that the command-line interface reveals.
"""
from . import database
from . import deduplicate
from . import inject
from . import list_command
from . import look
from . import plan
from . import process
from . import shell
from . import update
from . import watch

modules = [
    database,
    deduplicate,
    inject,
    list_command,
    look,
    plan,
    process,
    shell,
    update,
    watch,
]

def add_parsers(subparsers):
    """
    Add all sub-command parsers.
    """
    for module in modules:
        add_parser = getattr(module, 'add_parser')
        add_parser(subparsers)
