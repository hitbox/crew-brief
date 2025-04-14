"""
Styling for Excel workbooks.
"""
import pickle

from crew_brief.model.styling import Styling

def add_parser(subparsers):
    """
    Add parser for style sub-commands.
    """
    parser = subparsers.add_parser(
        'style',
        help = from_workbook.__doc__,
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
    parser.set_defaults(func=from_workbook)

def from_workbook(args):
    """
    Take styles from cells from a workbook using a prefix for named cells.
    """
    filename = args.file
    prefix = args.prefix
    styling = Styling.from_workbook(filename, prefix)
    with open('test.pickle', 'wb') as pickle_file:
        pickle.dump(styling, pickle_file)
