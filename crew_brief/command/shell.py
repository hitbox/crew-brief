import code

import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from crew_brief import configlib
from crew_brief.model import get_models

def add_parser(subparsers):
    """
    Add parser for shell command.
    """
    shell_parser = subparsers.add_parser(
        'shell',
        help = 'Interactive interpreter',
    )
    shell_parser.add_argument(
        '--run',
        help = 'Execute script before entering interactive interpreter.',
    )
    configlib.add_config_option(shell_parser)
    shell_parser.set_defaults(func=shell)

def shell(args):
    """
    Convenient interactive interpreter.
    """
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    engine = create_engine(database_uri)
    session = Session(engine)

    context = get_models()
    context.update({
        'sa': sa,
        'session': session,
    })

    if args.run:
        with open(args.run) as run_file:
            run_code = run_file.read()
        exec(run_code, context)

    code.interact(local=context)
