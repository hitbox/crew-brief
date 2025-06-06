import datetime

from crew_brief import configlib
from crew_brief import constants

def add_parser(subparsers):
    """
    Add sub-command parser for main run.
    """
    parser = subparsers.add_parser(
        'process',
        help = process.__doc__,
    )
    configlib.add_config_option(parser)
    parser.set_defaults(
        func = process,
    )

def substitutions():
    """
    Return substitution dict for format string.
    """
    now = datetime.datetime.now()
    today = now.date()
    one_day = datetime.timedelta(days=1)
    subs = {
        'now': now,
        'today': today,
        'yesterday': today - one_day,
    }
    return subs

def process(args):
    """
    Look for new files and process them.
    """
    # Read Python config file.
    config = configlib.pyfile_config(args.config)

    # Get processes list from it.
    processes = getattr(config, 'PROCESSES')

    subs = substitutions()
    for process in processes:
        process.run(subs)
