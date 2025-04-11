"""
Parse command line arguments and run sub-command.
"""

import argparse

from . import command

def add_drill_keys_argument(parser):
    """
    Add arguments drill keys.
    """
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
    """
    Add common --config option.
    """
    parser.add_argument(
        '--config',
        help =
            'Path to the configuration file. If not provided, the'
            ' CREW_BRIEF_CONFIG environment variable will be used.',
    )

def add_do_schema_option(parser):
    """
    Add option to use schema to convert types.
    """
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
    check_database_parser.set_defaults(func=command.database.check)
    add_config_option(check_database_parser)

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
    init_database_parser.set_defaults(func=command.database.init)
    add_config_option(init_database_parser)

def add_look_parser(subparsers):
    """
    Add parser for look command.
    """
    look_parser = subparsers.add_parser(
        'look',
        help = command.look.look.__doc__,
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
        func = command.look.look,
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
    sample_output_parser.set_defaults(func=command.sample.sample)
    add_config_option(sample_output_parser)

def add_unique_event_details_parser(subparsers):
    """
    Add parser for sub-command to find unique eventDetails.
    """
    parser = subparsers.add_parser(
        'unique_event_details',
        help = command.unique_event_details.unique_event_details.__doc__,
    )
    add_config_option(parser)
    add_do_schema_option(parser)
    parser.set_defaults(
        func = command.unique_event_details.unique_event_details,
    )

def add_process_parser(subparsers):
    """
    Add sub-command parser for main run.
    """
    parser = subparsers.add_parser(
        'process',
        help = command.process.process.__doc__,
    )
    add_config_option(parser)
    parser.set_defaults(
        func = command.process.process,
    )

def add_style_parser(subparsers):
    parser = subparsers.add_parser(
        'style',
        help = command.style.__doc__,
    )

    subparsers = parser.add_subparsers()

    help = 'Extract styles from a workbook.'
    from_workbook_parser = subparsers.add_parser(
        'from_workbook',
        help = help,
        description = help,
    )
    from_workbook_parser.add_argument(
        'file',
        help = 'Excel file.',
    )
    from_workbook_parser.add_argument(
        '--prefix',
        default = 'crew_brief__',
        help =
            'Prefix for named ranges to extract formatting from. Dots are not'
            ' allowed in named ranges. Default %(default)r.',
    )
    from_workbook_parser.add_argument(
        '--reference-suffix',
        default = 'reference',
        help = 'Suffix for the unaltered reference cell. Default %(default)r.',
    )
    parser.set_defaults(func=command.style.from_workbook)

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
    add_config_option(parser)

    subparsers = parser.add_subparsers()

    add_process_parser(subparsers)
    add_style_parser(subparsers)

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
