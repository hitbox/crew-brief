import os

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
