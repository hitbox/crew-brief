import configparser
import logging.config
import os
import pickle
import re
import sys
import types

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from pathlib import Path

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

def pyfile_config(filename, module_name='config'):
    """
    Load filename as Python module.
    """
    filename = Path(filename).resolve()
    spec = spec_from_file_location(module_name, filename)
    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def resolve_config(filename=None):
    if filename is None:
        filename = os.getenv(constants.ENVIRON_CONFIG_KEY)

    if filename is None:
        raise ValueError(f'Path to config not defined')

    return pyfile_config(filename)
