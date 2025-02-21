import argparse
import configparser
import copy
import datetime
import glob
import json
import logging.config
import os
import pickle
import re
import zipfile

from operator import itemgetter
from pprint import pprint

try:
    import win32com.client as win32
except ImportError:
    win32 = None

import jinja2
import marshmallow as mm
import openpyxl

from . import commands

def add_drill_keys_argument(parser):
    parser.add_argument(
        'keys',
        nargs = '+',
        help =
            'Sequence of keys into pickle database. Probably want "member_data'
            ' userEvents eventDetails"',
    )
    parser.add_argument(
        '--ignore-missing',
        action = 'store_true',
        help = 'Ignore missing keys.',
    )

def add_config_option(parser):
    parser.add_argument(
        '--config',
        help =
            'Path to the configuration file. If not provided, the'
            ' CREW_BRIEF_CONFIG environment variable will be used.',
    )

def add_do_schema_option(parser):
    parser.add_argument(
        '--schema',
        dest = 'schema',
        action = 'store_true',
        help = 'Convert string data from database.',
    )
    parser.add_argument(
        '--no-schema',
        dest = 'schema',
        action = 'store_false',
        help = 'Do not convert string data from database.',
    )
    parser.set_defaults(
        schema = True,
    )

def add_check_database_parser(subparsers):
    """
    Add check database sub-command parser.
    """
    check_database_parser = subparsers.add_parser(
        'check',
        help = 'Check assumptions against pickle database.',
        description =
            'Traverse the pickle database and confirm assumptions. That'
            ' eventDetails is a dict, for instance.',
    )
    check_database_parser.set_defaults(func=commands.check_database)
    add_config_option(check_database_parser)

def add_discover_structure_parser(subparsers):
    discover_structure_parser = subparsers.add_parser(
        'discover_structure',
        help = commands.discover_structure.__doc__,
    )
    add_drill_keys_argument(discover_structure_parser)
    add_do_schema_option(discover_structure_parser)
    add_config_option(discover_structure_parser)
    discover_structure_parser.set_defaults(
        func = commands.discover_structure,
    )

def add_init_database_parser(subparsers):
    """
    Add init database parser.
    """
    init_database_parser = subparsers.add_parser(
        'init',
        help = 'Initialize database.',
        description =
            'Initialize a database of JSON data from the ZIP files for'
            ' faster testing.',
    )
    init_database_parser.set_defaults(func=commands.init_database)
    add_config_option(init_database_parser)

def add_look_parser(subparsers):
    """
    Add parser for look command.
    """
    look_parser = subparsers.add_parser(
        'look',
        help = commands.look.__doc__,
    )
    look_parser.add_argument(
        '--unique',
        action = 'store_true',
        help = 'Print only unique values.',
    )
    add_drill_keys_argument(look_parser)
    add_do_schema_option(look_parser)
    add_config_option(look_parser)
    look_parser.set_defaults(
        func = commands.look,
    )

def add_sample_output_parser(subparsers):
    """
    Sample output parser.
    """
    sample_output_parser = subparsers.add_parser(
        'sample',
    )
    sample_output_parser.add_argument(
        'output',
        help = 'Format string to create path.',
    )
    sample_output_parser.add_argument(
        '-n', '--number',
        type = int,
        default = 5,
        help = 'Numbers of samples to produce.',
    )
    sample_output_parser.add_argument(
        '--autofit-with-excel',
        default = False,
        help = 'Use Excel to autofit workbook.',
    )
    sample_output_parser.add_argument(
        '--flattened',
        action = 'store_true',
        help =
            'Use single rows to write eventDetails to.'
            ' Otherwise create sub-tables.',
    )
    sample_output_parser.set_defaults(func=commands.sample_output)
    add_config_option(sample_output_parser)

def add_unique_event_details(subparsers):
    parser = subparsers.add_parser(
        'unique_event_details',
        help = commands.unique_event_details.__doc__,
    )
    add_config_option(parser)
    add_do_schema_option(parser)
    parser.set_defaults(
        func = commands.unique_event_details,
    )

def argument_parser():
    parser = argparse.ArgumentParser(
        prog = 'crew_brief',
        description =
            'Rewrite crew brief JSON files as more user friendly Excel files.',
    )
    add_config_option(parser)

    subparsers = parser.add_subparsers()

    add_check_database_parser(subparsers)
    add_discover_structure_parser(subparsers)
    add_init_database_parser(subparsers)
    add_look_parser(subparsers)
    add_sample_output_parser(subparsers)
    add_unique_event_details(subparsers)

    # Default to normal_run withoutput command given.
    parser.set_defaults(func=commands.normal_run)

    return parser

def run_from_args():
    """
    Parse command line and run sub-command.
    """
    parser = argument_parser()
    args = parser.parse_args()
    return args.func(args)
