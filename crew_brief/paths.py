import os

def walk_paths(top):
    for dirpath, dirnames, filenames in os.walk(top):
        for filename in filenames:
            yield os.path.normpath(os.path.join(dirpath, filename))
