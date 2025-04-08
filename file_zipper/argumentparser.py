import argparse

from . import command

def add_config_option(parser):
    parser.add_argument(
        '--config',
        nargs = '+',
        help = 'Paths to configuration.',
    )

def add_update_parser(subparsers):
    update_parser = subparsers.add_parser(
        'update',
        help = 'Update database.',
    )
    update_subparsers = update_parser.add_subparsers()

    # update paths
    update_paths_subparser = update_subparsers.add_parser(
        'paths',
        help = command.update.paths.__doc__,
    )
    update_paths_subparser.add_argument(
        '--from-file',
        help = 'Load paths from line separated file.',
    )
    update_paths_subparser.set_defaults(command=command.update.paths)

    # update matches
    update_path_match_subparser = update_subparsers.add_parser(
        'matches',
        help = command.update.matches.__doc__,
    )
    update_path_match_subparser.set_defaults(command=command.update.matches)

    # update data (order), that is reapply schema to data
    update_data_subparser = update_subparsers.add_parser(
        'data',
        help = command.update.data.__doc__,
    )
    update_data_subparser.set_defaults(command=command.update.data)

def add_check_parser(subparsers):
    check_parser = subparsers.add_parser(
        'check',
        help = 'Check various conditions.',
    )
    check_subparsers = check_parser.add_subparsers()
    check_assume_parser = check_subparsers.add_parser(
        'assume',
    )
    check_assume_parser.add_argument(
        '--path-parser',
        action = 'append',
        help = 'Path parser name to check assumptions against.',
    )
    check_assume_parser.set_defaults(command=command.check.assumptions)

def add_database_parser(subparsers):
    """
    Add database (db) sub-command parser.
    """
    init_parser = subparsers.add_parser(
        'db',
        help = 'Database sub-commands.',
    )
    init_subparsers = init_parser.add_subparsers()
    init_db_parser = init_subparsers.add_parser('init')
    init_db_parser.add_argument(
        'pyfile',
        help = 'Python script adds initial database objects.',
    )
    init_db_parser.set_defaults(command=command.db.init)

def add_shell_parser(subparsers):
    shell_parser = subparsers.add_parser(
        'shell',
        help = 'Interactive shell.',
    )
    shell_parser.set_defaults(command=command.shell)

def add_query_parser(subparsers):
    query_parser = subparsers.add_parser(
        'query',
        help = 'Interesting queries.',
    )
    query_parser.set_defaults(command=command.shell)
    query_subparsers = query_parser.add_subparsers()
    least_similar_paths_parser = query_subparsers.add_parser('least_similar_paths')
    least_similar_paths_parser.add_argument(
        '--limit',
        type = int,
        default = 10,
    )
    least_similar_paths_parser.set_defaults(command=command.query.least_similar_paths)

def parser():
    parser = argparse.ArgumentParser(
        prog = 'file_zipper',
        description = '',
    )
    add_config_option(parser)
    subparsers = parser.add_subparsers(dest='command')
    add_update_parser(subparsers)
    add_check_parser(subparsers)
    add_database_parser(subparsers)
    add_shell_parser(subparsers)
    add_query_parser(subparsers)

    return parser
