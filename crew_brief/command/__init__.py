"""
Functions for the commands that the command-line interface reveals.
"""
from . import inject
from . import look
from . import process
from . import watch

def add_parsers(subparsers):
    """
    Add all sub-command parsers.
    """
    inject.add_parser(subparsers)
    look.add_parser(subparsers)
    process.add_parser(subparsers)
    watch.add_parser(subparsers)
