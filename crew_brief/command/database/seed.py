from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import configlib

def add_parser(subparsers):
    parser = subparsers.add_parser(
        'seed',
        help = db_seed.__doc__,
    )
    parser.add_argument(
        '--seed-func',
        default = 'seed',
        help = 'Name of seed func to call from config. Default: %(default)r',
    )
    parser.add_argument(
        '--commit',
        action = 'store_true',
        help = 'Commit changes.',
    )
    configlib.add_config_option(parser)
    parser.set_defaults(func=db_seed)

def db_seed(args):
    """
    Seed database with initial data.
    """
    config = configlib.resolve_config(args.config)

    # Get names from config as early as possible, raising for missing.
    database_uri = getattr(config, 'DATABASE_URI')
    seed_func = getattr(config, args.seed_func)

    engine = create_engine(database_uri)
    with Session(engine) as session:
        seed_func(session)
        if args.commit:
            session.commit()
