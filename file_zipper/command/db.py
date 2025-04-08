import importlib.util

from file_zipper import configlib
from file_zipper.model import Base

def init(parser, args):
    """
    Initialize database with seed data. Take one argument to a Python file with
    a function `seed` that adds the objects.
    """
    cp = configlib.config_from_args(args)
    session = configlib.session_from_config(cp)

    Base.metadata.create_all(session.get_bind())

    # Execute script to initialize database objects.
    spec = importlib.util.spec_from_file_location('seed_module', args.pyfile)
    seed_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(seed_module)
    seed_module.seed(session)

    # Commit new objects
    session.commit()
