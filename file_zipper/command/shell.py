import code

import sqlalchemy.orm

from file_zipper import configlib
from file_zipper.model import ExcludedPath
from file_zipper.model import FileType
from file_zipper.model import Glob
from file_zipper.model import Path
from file_zipper.model import Regex

sa = sqlalchemy

def shell(parser, args):
    """
    Load database with all globbed paths.
    """
    cp = configlib.config_from_args(args)
    session = configlib.session_from_config(cp)

    local = {
        'sa': sa,
        'ExcludedPath': ExcludedPath,
        'FileType': FileType,
        'Glob': Glob,
        'Path': Path,
        'Regex': Regex,
        'session': session,
    }

    code.interact(local=local)
