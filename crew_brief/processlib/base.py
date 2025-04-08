import copy
import io
import json
import logging
import re

from abc import ABC
from abc import abstractmethod
from zipfile import ZipFile

from crew_brief.paths import setdefault_for_base_path
from crew_brief.schema import UserEventsSchema
from crew_brief.workbook import build_workbook_for_member

class Process(ABC):
    """
    Abstract class requiring a run method.
    """

    @classmethod
    @abstractmethod
    def from_config(cls, cp, name):
        pass

    @abstractmethod
    def run(self):
        pass
