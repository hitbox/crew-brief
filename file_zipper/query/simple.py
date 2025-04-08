import sqlalchemy as sa

from file_zipper.model import Path

def paths_without_match():
    """
    Select statement for paths that failed to match regex.
    """
    stmt = sa.select(
        Path,
    ).filter(
        Path.data == None,
    )
    return stmt
