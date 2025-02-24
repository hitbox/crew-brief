"""
Loading the pickle database functions.
"""

import pickle

from . import constants

def database_path(config):
    """
    Return the path to the pickle database from config.
    """
    database_fn = config[constants.NAME]['database']
    return database_fn

def database_from_config(config):
    """
    Load and return the object from the pickle database.
    """
    database_fn = database_path(config)
    with open(database_fn, 'rb') as database_file:
        database = pickle.load(database_file)
    return database
