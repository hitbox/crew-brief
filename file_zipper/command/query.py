import code
import difflib

import sqlalchemy.orm

from file_zipper import configlib
from file_zipper.model import ExcludedPath
from file_zipper.model import FileType
from file_zipper.model import Glob
from file_zipper.model import Path
from file_zipper.model import Regex

sa = sqlalchemy

def least_similar_paths(parser, args):
    # TODO
    # - Motivation here is to list the most dissimilar paths for examples to
    #   the regexes.
    cp = configlib.config_from_args(args)
    session = configlib.session_from_config(cp)

    paths = session.scalars(sa.select(Path.path).limit(args.limit)).all()
    raise NotImplementedError
