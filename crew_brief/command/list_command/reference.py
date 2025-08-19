from pprint import pprint

import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import configlib
from crew_brief import model as modellib
from crew_brief.model import Base
from crew_brief.model import get_model_by_table_name
from crew_brief.model import get_references

def add_parser(subparsers):
    # Sub-command to list object that reference an object.
    parser = subparsers.add_parser('ref')
    configlib.add_config_option(parser)
    parser.add_argument('obj', help='Model or table name.')
    parser.set_defaults(func=list_references)

def list_references(args):
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    engine = create_engine(database_uri)
    with Session(engine) as session:

        model = get_model_by_table_name(args.obj)
        if not model:
            model = getattr(modellib, args.obj)

        pprint(list(get_references(model)))
