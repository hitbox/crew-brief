import configparser
import logging.config
import os
import pickle
import re
import types

from . import constants

def add_config_option(parser):
    """
    Add common --config option.
    """
    parser.add_argument(
        '--config',
        help =
            'Path to the configuration file. If not provided, the'
            ' CREW_BRIEF_CONFIG environment variable will be used.',
    )

def from_args(args):
    """
    Resolve configuration from command line arguments.
    """
    if args.config:
        config_path = args.config
    elif constants.ENVIRON_CONFIG_KEY in os.environ:
        config_path = os.getenv(constants.ENVIRON_CONFIG_KEY)
    else:
        config_path = []

    if not config_path:
        raise ValueError('No configuration files given or found.')

    cp = configparser.ConfigParser(
        interpolation = configparser.ExtendedInterpolation(),
    )
    cp.read(config_path)

    if set(['loggers', 'handlers', 'formatters']).issubset(cp):
        logging.config.fileConfig(cp)
    else:
        logging.basicConfig(level=logging.INFO)

    return cp

def instance_from_config(cp, secname, prefix, globals=None, locals=None):
    """
    Eval to instantiate from config.
    """
    section = cp[f'{prefix}{secname}']
    class_ = eval(section['class'], globals, locals)
    args = eval(section.get('args', 'tuple()'), globals, locals)
    kwargs = eval(section.get('kwargs', 'dict()'), globals, locals)
    return class_(*args, **kwargs)

def pyfile_config(filename):
    """
    Load filename as Python module.
    """
    config = types.ModuleType('config')
    with open(filename, 'r') as config_file:
        code = config_file.read()
    try:
        exec(code, config.__dict__)
    except Exception as e:
        raise Exception(f'Error in config file {filename}.')
    return config

def resolve_config(filename=None):
    if filename is None:
        filename = os.getenv(constants.ENVIRON_CONFIG_KEY)

    if filename is None:
        raise ValueError(f'Path to config not defined')

    return pyfile_config(filename)
