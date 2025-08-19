import os
import sys

app_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(app_dir)
instance_dir = os.path.join(project_dir, 'instance')
config_dir = os.path.join(instance_dir, 'config')
logging_dir = os.path.join(instance_dir, 'logging')

executable_dir = os.path.dirname(sys.executable)
pythonw_path = os.path.normpath(os.path.join(executable_dir, 'pythonw.exe'))
flask_path = os.path.normpath(os.path.join(executable_dir, 'flask.exe'))

def walk_paths(top):
    """
    Generate full, normalized paths from os.walk.
    """
    for dirpath, dirnames, filenames in os.walk(top):
        for filename in filenames:
            yield os.path.normpath(os.path.join(dirpath, filename))

def setdefault_for_base_path(data, path):
    """
    Parse the base parts of path out and update data with setdefault.
    """
    basename = os.path.basename(path)
    baseroot, baseext = os.path.splitext(basename)
    data.setdefault('basename', basename)
    data.setdefault('baseroot', baseroot)
    data.setdefault('baseext', baseext)
