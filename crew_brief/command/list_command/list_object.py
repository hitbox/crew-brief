import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import configlib
from crew_brief.model import get_models

class ListCommand:
    """
    Callable prints the names of objects in database.
    """

    def __init__(self, model):
        self.model = model

    def __call__(self, args):
        config = configlib.resolve_config(args.config)
        database_uri = getattr(config, 'DATABASE_URI')
        engine = create_engine(database_uri)
        with Session(engine) as session:
            stmt = sa.select(self.model).order_by(self.model.name)
            for instance in session.scalars(stmt):
                if hasattr(instance, 'describe_short'):
                    print(instance.describe_short())
                elif hasattr(instance, 'name'):
                    print(instance.name)
                else:
                    print(instance)


def add_commands(list_subparsers):
    # Add sub-commands to list names of models that have a name attribute.
    # TODO
    # - Instead of sub-commands, use an argument.
    for name, model in get_models().items():
        if hasattr(model, 'name'):
            parser_name = model.__tablename__
            model_list_parser = list_subparsers.add_parser(parser_name, help=model.__doc__)
            configlib.add_config_option(model_list_parser)
            model_list_parser.set_defaults(func=ListCommand(model))
