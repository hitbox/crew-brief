from . import file_index
from . import os_walk
from . import parse
from . import zip_complete

modules = [
    file_index,
    os_walk,
    parse,
    zip_complete,
]

def add_parser(subparsers):
    """
    Add sub-command parser for indexing files.
    """
    parser = subparsers.add_parser(
        'update',
        help = 'Update database commands.',
    )

    update_subparsers = parser.add_subparsers()

    for module in modules:
        add_parser = getattr(module, 'add_parser')
        add_parser(update_subparsers)
