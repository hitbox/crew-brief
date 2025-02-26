"""
Functions for the commands that the command-line interface reveals.
"""
import copy
import pickle

from pprint import pprint

import openpyxl

from crew_brief import configlib
from crew_brief import constants
from crew_brief import databaselib
from crew_brief import nodes
from crew_brief import schema

from .check_database import check_database
from .init_database import init_database
from .look import look
from .sample_output import sample_output
from .unique_event_details import unique_event_details

def normal_run(args):
    """
    Look for new files and process them.
    """
    # TODO
    print('normal_run')
    config = configlib.from_args(args)
    pprint(config)
