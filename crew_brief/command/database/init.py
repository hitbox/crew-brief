from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import completeness
from crew_brief import configlib
from crew_brief.model import Base

def add_parser(subparsers):
    """
    """
    init_parser = subparsers.add_parser('init', help=db_init.__doc__)
    configlib.add_config_option(init_parser)
    init_parser.set_defaults(func=db_init)

def db_init(args):
    """
    Initialize crew brief database.
    """
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)
