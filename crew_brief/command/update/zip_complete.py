from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import configlib
from crew_brief.completeness import update_required_members

def add_parser(parsers):
    """
    Add zip complete command.
    """
    parser = parsers.add_parser(
        'zip_complete',
        help = zip_complete.__doc__,
    )
    parser.add_argument(
        'zip_spec',
        help = 'Name of ZipSpec object.',
    )
    parser.add_argument(
        '--batch-size',
        type = int,
        default = 100,
    )
    configlib.add_config_option(parser)
    parser.set_defaults(func=zip_complete)

def zip_complete(args):
    """
    Update completeness of zip files.
    """
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    engine = create_engine(database_uri)
    with Session(engine) as session:
        update_required_members(session, args.zip_spec, args.batch_size)
