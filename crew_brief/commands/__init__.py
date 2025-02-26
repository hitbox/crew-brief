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

from .init_database import init_database
from .look import look
from .sample_output import sample_output

def check_database(args):
    """
    Check assumptions against pickle database.
    """
    config = configlib.from_args(args)
    database = databaselib.database_from_config(config)
    typed_database = schema.pickle_schema.load(
        database,
        many = True,
    )

    for zip_data in typed_database:
        member_data = zip_data.get('member_data')
        assert isinstance(user_event['eventDetails'], dict)

def normal_run(args):
    """
    Look for new files and process them.
    """
    # TODO
    print('normal_run')
    config = configlib.from_args(args)
    pprint(config)

def unique_event_details(args):
    config = configlib.from_args(args)
    database = databaselib.database_from_config(config)
    structures = set()
    for zip_data in database:
        if args.schema:
            # Load/typify one at a time for quick results.
            zip_data = schema.pickle_schema.load(zip_data)
        member_data = zip_data['member_data']
        if member_data:
            user_events = member_data['userEvents']
            for user_event in user_events:
                event_details = user_event.get('eventDetails')
                if event_details:
                    # Add keys.
                    structures.add(tuple(event_details))
    pprint(structures)
