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
    config = types.ModuleType('config')
    with open(filename, 'r') as config_file:
        code = config_file.read()
    exec(code, config.__dict__)
    return config

