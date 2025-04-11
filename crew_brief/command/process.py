import datetime
import importlib
import inspect
import types

from crew_brief import configlib
from crew_brief import constants
from crew_brief import processlib
from crew_brief.model import eval_context

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

def resolve_name(name):
    module_path, _, attrname = name.rpartition('.')
    module = importlib.import_module(module_path)
    return getattr(module, attrname)

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

        class_ = resolve_name(process_classes[class_name])
        args = eval(process_section.get('args', '()'), eval_context)
        kwargs = eval(process_section.get('kwargs', '{}'), eval_context)
        process = class_(*args, **kwargs)

        processes[process_name] = process

    return processes

def process(args):
    """
    Look for new files and process them.
    """
    # Read Python config file.
    config = types.ModuleType('config')
    with open(args.config, 'r') as config_file:
        code = config_file.read()
    exec(code, config.__dict__)

    # Get processes list from it.
    processes = getattr(config, 'PROCESSES')

    subs = substitutions()
    for process in processes:
        process.run(subs)
