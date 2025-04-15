"""
Functions for the commands that the command-line interface reveals.
"""
from . import look
from . import process

def add_parsers(subparsers):
    """
    Add all sub-command parsers.
    """
    look.add_parser(subparsers)
    process.add_parser(subparsers)
