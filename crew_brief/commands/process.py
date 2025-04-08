import datetime
import inspect
import os

from crew_brief import configlib
from crew_brief import constants
from crew_brief import processlib
from crew_brief.paths import walk_paths

def substitutions():
    """
    Return substitution dict for format string.
    """
    now = datetime.datetime.now()
    today = now.date()
    one_day = datetime.timedelta(days=1)
    subs = {
        'now': now,
        'today': today,
        'yesterday': today - one_day,
    }
    return subs

def _classes_for_processes():
    """
    Return the valid process classes as dict.
    """

    def is_process_class(obj):
        return (
            inspect.isclass(obj)
            and
            issubclass(obj, processlib.Process)
            and
            obj is not processlib.Process
        )

    return dict(inspect.getmembers(processlib, predicate=is_process_class))

def file_config(cp):
    """
    Return dict of named processes to run.
    """
    processes = {}
    process_classes = _classes_for_processes()
    for process_name in configlib.human_split(cp[constants.NAME]['processes']):
        if process_name in processes:
            raise ValueError(f'Duplicate process name: {process_name}.')

        process_section = cp['process.' + process_name]

        class_name = process_section['class']

        if class_name not in process_classes:
            raise NameError(f'Invalid process class name {class_}.')

        class_ = process_classes[class_name]
        process = class_.from_config(cp, process_name, process_section)

        processes[process_name] = process

    return processes

def process(args):
    """
    Look for new files and process them.
    """
    config = configlib.from_args(args)
    processes = file_config(config)

    subs = substitutions()
    for process_name, process in processes.items():
        process.run(subs)
