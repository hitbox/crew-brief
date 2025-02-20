import configparser
import logging.config
import os
import pickle

from . import constants

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

    cp = configparser.ConfigParser()
    cp.read(config_path)

    if set(['loggers', 'handlers', 'formatters']).issubset(cp):
        logging.config.fileConfig(cp)

    return cp

def iter_numbered_prefix(data, prefix):
    for key, val in data.items():
        if key.startswith(prefix) and key[len(prefix):].isdigit():
            yield (key, val)

def get_tops_and_regexes(cp):
    for _, suffix in iter_numbered_prefix(cp[constants.NAME], 'top'):
        section = cp[f'top.{suffix}']
        top = section['top']
        path_data_regex = re.compile(section['path_pattern'])
        yield (top, path_data_regex)

def instance_from_config(cp, secname, prefix, globals=None, locals=None):
    """
    Eval to instantiate from config.
    """
    section = cp[f'{prefix}{secname}']
    class_ = eval(section['class'], globals, locals)
    args = eval(section.get('args', 'tuple()'), globals, locals)
    kwargs = eval(section.get('kwargs', 'dict()'), globals, locals)
    return class_(*args, **kwargs)

def split_sections(string):
    return string.split()

