import enum
import ntpath
import os
import posixpath

class PathFlavor(enum.Enum):
    """
    Enumerate common path flavors with associated module for manipulating them.
    """
    auto = 'auto'
    posix = 'posix'
    nt = 'nt'

    def __init__(self, name):
        if name == 'auto':
            self.module = os.path
        elif name == 'posix':
            self.module = posixpath
        elif name == 'nt':
            self.module = ntpath

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattr__(name)
        else:
            return getattr(self.module, name)
