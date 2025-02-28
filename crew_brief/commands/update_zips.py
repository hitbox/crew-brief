import datetime
import os

from crew_brief import configlib
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

def update_zips(args):
    """
    Look for new files and process them.
    """
    config = configlib.from_args(args)
    processes = configlib.file_config(config)

    subs = substitutions()
    for process_name, process in processes.items():
        process.run(subs)
