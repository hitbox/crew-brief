from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from crew_brief import configlib
from crew_brief.model import OSWalk
from crew_brief.index import index_files

def add_parser(parsers):
    parser = parsers.add_parser(
        'file_index',
        help = file_index_command.__doc__,
    )
    parser.add_argument(
        '--all',
        action = 'store_true',
        help = 'Index files from all file walkers.',
    )
    parser.add_argument(
        '--commit',
        action = 'store_true',
        help = 'Commit changes.',
    )
    parser.add_argument(
        'os_walk',
        nargs = '*',
        help = 'Names of OSWalk objects (ignored if --all is passed).',
    )
    configlib.add_config_option(parser)
    parser.set_defaults(func=file_index_command)

def file_index_command(args):
    """
    Save new paths to database.
    """
    if not args.os_walk and not args.all:
        raise ValueError('Must specify --all or give file walker names.')

    # Read Python config file and get database uri.
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')

    engine = create_engine(database_uri)
    with Session(engine) as session:

        if args.all:
            walkers = session.scalars(select(OSWalk)).all()
        else:
            walkers = [OSWalk.by_name(name) for name in args.os_walk]

        index_files(session, walkers)
        if args.commit:
            session.commit()
