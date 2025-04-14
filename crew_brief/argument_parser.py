"""
Parse command line arguments and run sub-command.
"""

import argparse

from crew_brief import command
from crew_brief import configlib

def argument_parser():
    """
    Create the argument parser.
    """
    parser = argparse.ArgumentParser(
        prog = 'crew_brief',
        description =
            'Create user friendly Excel from JSON and write back'
            ' into ZIP files.',
    )
    configlib.add_config_option(parser)

    # Add sub-command parsers.
    subparsers = parser.add_subparsers()
    command.add_parsers(subparsers)

    # Default to update_zips withoutput command given.
    parser.set_defaults(func=command.process.process)

    return parser

def run_from_args():
    """
    Parse command line and run sub-command.
    """
    parser = argument_parser()
    args = parser.parse_args()
    func = args.func
    delattr(args, 'func')
    return func(args)
