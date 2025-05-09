from .base import Process
from .mixin import PathMixin

class WatchProcess(Process, PathMixin):
    """
    Index and check ZIP files for changes and notify when they are complete.
    """

    def __init__(self, sources):
        self.sources = sources

    def run(self, subs):
        for path_data in self._generate_paths(subs):
            print(path_data)
