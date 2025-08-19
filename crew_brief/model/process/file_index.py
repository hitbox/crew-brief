import os

from pprint import pprint

import sqlalchemy as sa

from sqlalchemy.orm import Session

from crew_brief.model import LegFile

from .base import Process
from .mixin import PathMixin

class RegexNoMatch(ValueError):
    """
    Regular expression did not match.
    """


class FileIndexProcess(Process, PathMixin):
    """
    Index files, especially paths.
    """

    def __init__(self, sources, database_uri, ignore=None):
        """
        :param sources:
            Produces file listings.
        :param database_uri:
            Database URI to use for a session.
        :param ignore:
            Literal, normalized paths to ignore.
        """
        self.sources = sources
        self.database_uri = database_uri
        if ignore is None:
            ignore = set()
        self.ignore = ignore

    def run(self, subs):
        engine = sa.create_engine(self.database_uri)
        with Session(engine) as session:
            # Load existing strings into sets.
            existing_paths = set(session.scalars(sa.select(LegFile.path)))
            new_objects = set()
            for path_data in self._generate_paths(subs, normalize=os.path.normpath):
                if path_data.path in self.ignore:
                    # Skip paths to ignore.
                    continue

                if path_data.path not in existing_paths:
                    # Add new file path.
                    leg_file = LegFile(path=path_data.path)
                    new_objects.add(leg_file)

            session.bulk_save_objects(new_objects)
            session.commit()
