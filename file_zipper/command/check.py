import sqlalchemy as sa

from file_zipper import configlib
from file_zipper.model import Glob
from file_zipper.model import Path

def assumptions(parser, args):
    """
    Check assumptions about path data.
    """
    cp = configlib.config_from_args(args)
    session = configlib.session_from_config(cp)
    raise NotImplementedError
