from textwrap import dedent

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import configlib
from crew_brief.parse import parse_leg_identifiers

def add_parser(parsers):
    parser = parsers.add_parser('parse', help=parse_filenames.__doc__)
    parser.add_argument(
        'os_walk',
        help = dedent(
            '''
            Name of OSWalk object to select paths from database. Use list
            command to list names.
            '''.strip()
        ),
    )
    parser.add_argument(
        'scraper',
        help = dedent(
            '''
            Name of Scraper object to scrape and deserialize paths. Use list
            command to list their names.
            '''.strip()
        ),
    )
    parser.add_argument(
        '--force',
        action = 'store_true',
        help = 'Force parsing all files for os_walk and scraper.',
    )
    parser.add_argument(
        '--raise',
        action = 'store_true',
        help = 'Raise errors. Silent by default.',
    )
    parser.add_argument(
        '--commit',
        action = 'store_true',
        help = 'Commit changes',
    )
    configlib.add_config_option(parser)
    parser.set_defaults(func=parse_filenames)

def parse_filenames(args):
    """
    Parse file paths generated from a named OSWalk object against a named Scraper object.
    """
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    engine = create_engine(database_uri)
    with Session(engine) as session:
        parse_leg_identifiers(
            session,
            args.os_walk,
            args.scraper,
            force=args.force,
            silent = not getattr(args, 'raise'),
        )
        if args.commit:
            session.commit()
