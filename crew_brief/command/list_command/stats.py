import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import completeness
from crew_brief import configlib
from crew_brief.model import Base
from crew_brief.model import LegFile

def add_parser(subparsers):
    """
    Add sub-command parser for listing stats.
    """
    list_stats_parser = subparsers.add_parser('stats', help=list_stats.__doc__)
    configlib.add_config_option(list_stats_parser)
    list_stats_parser.set_defaults(func=list_stats)

def list_stats(args):
    """
    Show stats for complete/incomplete zip files.
    """
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    engine = create_engine(database_uri)
    with Session(engine) as session:
        is_complete = (LegFile.complete_at.is_not(None)).label('is_complete')
        results = session.execute(
            sa.select(is_complete, sa.func.count()).group_by(is_complete)
        ).all()
        for is_complete, count in results:
            print(f'Complete: {is_complete}, Count: {count:,}')
