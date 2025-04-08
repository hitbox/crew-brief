import configparser
import logging.config
import os
import pickle
import re

from . import constants
from crew_brief.models import eval_context

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
        raise ValueError('No configuration files given.')

    cp = configparser.ConfigParser(
        interpolation = configparser.ExtendedInterpolation(),
    )
    cp.read(config_path)

    if set(['loggers', 'handlers', 'formatters']).issubset(cp):
        logging.config.fileConfig(cp)
    else:
        logging.basicConfig(level=logging.INFO)

    return cp

def iter_numbered_prefix(data, prefix):
    """
    Generate key-value pairs of a section whose keys have a prefix or optional
    digit suffix.
    """
    for key, val in data.items():
        if key.startswith(prefix) and key[len(prefix):].isdigit():
            yield (key, val)

def instance_from_config(cp, secname, prefix, globals=None, locals=None):
    """
    Eval to instantiate from config.
    """
    section = cp[f'{prefix}{secname}']
    class_ = eval(section['class'], globals, locals)
    args = eval(section.get('args', 'tuple()'), globals, locals)
    kwargs = eval(section.get('kwargs', 'dict()'), globals, locals)
    return class_(*args, **kwargs)

def human_split(string):
    return string.replace(',', ' ').split()

def get_member_re(config):
    return re.compile(config[constants.NAME]['member'])

def get_tops_and_regexes(cp):
    """
    Generate top dirs for os.walk
    """
    for _, suffix in iter_numbered_prefix(cp[constants.NAME], 'top'):
        section = cp[f'top.{suffix}']
        top = section['top']
        path_data_regex = re.compile(section['path_pattern'])
        yield (top, path_data_regex)

def instance_section(section, context):
    class_ = eval(section['class'], None, context)
    args = eval(section.get('args', '()'), None, context)
    kwargs = eval(section.get('kwargs', '{}'), None, context)
    instance = class_(*args, **kwargs)
    return instance
