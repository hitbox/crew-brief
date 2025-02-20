import pickle

from . import constants

def database_path(config):
    database_fn = config[constants.NAME]['database']
    return database_fn

def database_from_config(config):
    database_fn = database_path(config)
    with open(database_fn, 'rb') as database_file:
        database = pickle.load(database_file)
    return database
