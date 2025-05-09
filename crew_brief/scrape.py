import re

from abc import ABC
from abc import abstractmethod

class ScrapeBase(ABC):
    @abstractmethod
    def __call__(self):
        pass


class ScrapePath(ScrapeBase):

    def __init__(self, filename_regex):
        self.filename_regex = filename_regex

    def __call__(self, path):
        breakpoint()
        pass


log_level_pilot_docs_filename_regex = re.compile('')
