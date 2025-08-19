from . import append_zip

command_modules = [
    append_zip,
]

def add_parser(subparsers):
    """
    Add sub-command parsers for planning commands.
    """
    parser = subparsers.add_parser(
        'plan',
        help = 'Commands to plan new file operations.',
    )

    plan_subparsers = parser.add_subparsers()

    for module in command_modules:
        add_parser = getattr(module, 'add_parser')
        add_parser(plan_subparsers)
