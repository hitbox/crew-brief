import sqlalchemy as sa

from file_zipper import configlib
from file_zipper.model import ExcludedPath
from file_zipper.model import FileType
from file_zipper.model import Glob
from file_zipper.model import Path
from file_zipper.model import Regex

def _from_file(file_path):
    with open(args.from_file) as paths_file:
        for line in paths_file:
            yield line.strip()

def _from_globs(session):
    for globobj in session.query(Glob):
        for path in globobj.iglob():
            yield path

def paths(parser, args):
    """
    Load database with all globbed paths.
    """
    cp = configlib.config_from_args(args)
    session = configlib.session_from_config(cp)

    existing = {pathobj.path for pathobj in session.query(Path)}
    excluded = {excluded.path for excluded in session.query(ExcludedPath)}

    if args.from_file:
        paths_iter = _from_file(args.from_file)
    else:
        paths_iter = _from_globs(session)

    for path in paths_iter:
        if path not in existing and path not in excluded:
            pathobj = Path(
                path = path,
                file_type = FileType.from_filename(path, session),
                glob = globobj,
            )
            session.add(pathobj)

    session.commit()

def matches(parser, args):
    """
    Update regex matched data from paths loaded in database.
    """
    cp = configlib.config_from_args(args)
    session = configlib.session_from_config(cp)

    stmt = sa.select(Path).where(Path.data == None)
    for fileobj in session.scalars(stmt):
        if fileobj.glob:
            # Check for missing glob, the path may be manually inserted.
            for regexobj in fileobj.glob.regexes:
                match = regexobj.compiled.match(fileobj.path)
                if match:
                    path_data = regexobj.schema.instance.load(match.groupdict())
                    fileobj.data = path_data
                    break

    session.commit()

def data(parser, args):
    """
    Reapply the schema to the PathMatch data column.
    """
    cp = configlib.config_from_args(args)
    session = configlib.session_from_config(cp)

    for path_match in session.scalars(sa.select(PathMatch)):
        regex = path_match.path_parser.regex.compiled
        schema = path_match.path_parser.schema.instance
        # Match should always happen.
        match = regex.match(path_match.path.path)
        data = schema.load(match.groupdict())
        data = schema.dump(data)
        path_match.data = data

    session.commit()
