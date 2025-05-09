from .base import Process
from .mixin import PathMixin

class InjectProcess(Process, PathMixin):
    """
    Inject files into zip files.
    """

    def __init__(self, sources, scraper):
        self.sources = sources
        self.scraper = scraper

    def run(self, subs):
        for path_data in self._generate_paths(subs):
            scrape_data = self.scraper(path_data)
