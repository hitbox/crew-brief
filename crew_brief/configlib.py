import configparser
import logging.config
import os
import pickle
import re

from . import constants
from crew_brief.process import UpdateUserFriendlyProcess
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

def split_sections(string):
    return string.split()

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

def get_rundata(config):
    """
    Main update zips runtime data.
    """
    rundata = {
        'tops_and_regexes': list(get_tops_and_regexes(config)),
        'member_re': re.compile(config[constants.NAME]['member']),
    }
    return rundata

def instance_section(section, context):
    class_ = eval(section['class'], None, context)
    args = eval(section.get('args', '()'), None, context)
    kwargs = eval(section.get('kwargs', '{}'), None, context)
    instance = class_(*args, **kwargs)
    return instance

def file_config(cp, process_class=UpdateUserFriendlyProcess):
    """
    Return dict of named processes to run.
    """
    processes = {}
    sources = {}
    archives = {}
    writers = {}
    member_regexes = {}
    path_data_regexes = {}

    for process_name in human_split(cp[constants.NAME]['processes']):
        if process_name in processes:
            raise ValueError(f'Duplicate process name: {process_name}.')

        process_section = cp['process.' + process_name]

        # Required regex to match member for JSON file.
        member_re_name = process_section['member_re']
        if member_re_name not in member_regexes:
            member_re_section = cp['zip_member_re.' + member_re_name]
            member_re = re.compile(member_re_section['member_re'])
            member_regexes[member_re_name] = member_re
        member_re = member_regexes[member_re_name]

        # Required writer key to section.
        writer_name = process_section['writer']
        if writer_name not in writers:
            # Update writer named dict.
            writer_section = cp['writer.' + writer_name]
            writers[writer_name] = instance_section(writer_section, eval_context)
        writer = writers[writer_name]

        # Optional path_data_re regex.
        if 'path_data' in process_section:
            path_data_name = process_section['path_data']
            if path_data_name not in path_data_regexes:
                path_data_section = cp['path_data.' + path_data_name]
                path_data_re = re.compile(path_data_section['path_data_re'])
                path_data_regexes[path_data_name] = path_data_re
            path_data_re = path_data_regexes[path_data_name]
        else:
            path_data_re = None

        # List of source objects for this process.
        sources_list = []
        for source_name in human_split(process_section['sources']):
            if source_name not in sources:
                # Update named sources dict.
                source_section = cp['source.' + source_name]
                sources[source_name] = instance_section(source_section, eval_context)
            # Add source for process.
            sources_list.append(sources[source_name])

        # Archive after processing object.
        archive_name = process_section['archive']
        if archive_name not in archives:
            # Update named archive dict.
            archive_section = cp['archive.' + archive_name]
            archives[archive_name] = instance_section(archive_section, eval_context)
        archive = archives[archive_name]

        process = process_class(
            sources = sources_list,
            member_re = member_re,
            writer = writer,
            archive = archive,
            path_data_re = path_data_re,
        )
        processes[process_name] = process

    return processes
