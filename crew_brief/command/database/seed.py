from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import completeness
from crew_brief import configlib
from crew_brief.model import Base

def add_parser(subparsers):
    db_seed_parser = subparsers.add_parser(
        'seed',
        help = db_seed.__doc__,
    )
    db_seed_parser.add_argument(
        '--seed_func',
        default = 'seed',
        help = 'Name of seed func to call from config.',
    )
    configlib.add_config_option(db_seed_parser)
    db_seed_parser.set_defaults(func=db_seed)

def db_seed(args):
    """
    Seed database with initial data.
    """
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    seed_func = getattr(config, args.seed_func)

    engine = create_engine(database_uri)
    with Session(engine) as session:
        seed_func(session)
