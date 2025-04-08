import sqlalchemy as sa

from file_zipper import configlib
from file_zipper.model import Glob
from file_zipper.model import Path
from file_zipper.model import PathMatch
from file_zipper.model import PathParser

def match_paths(parser, args):
    """
    TODO
    Attempt to match ZIP paths to PDF paths.
    """
    cp = configlib.config_from_args(args)
    session = configlib.session_from_config(cp)

    for pathobj in session.query(Path):
        path_parser = session.query(
            PathParser,
        ).filter(
            PathParser.glob_id == pathobj.glob_id,
        ).one()
        match = path_parser.match(pathobj.path)
        if match:
            path_match = PathMatch(
                path = pathobj,
                path_parser = path_parser,
                data = match.groupdict(),
            )
            session.add(path_match)
