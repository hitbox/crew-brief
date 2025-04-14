"""
Look for interesting data from the JSON files.
"""

from . import nodes

def has_list(data):
    """
    Recursively find a list in nested data.
    """
    for value in data.values():
        if isinstance(value, (list, tuple)):
            return True
        if isinstance(value, dict):
            if has_list(value):
                return True
    return None
