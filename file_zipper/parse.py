import re

from collections import defaultdict

# Regex to capture the components (named groups, literals, etc.)
# This will capture named groups and other components like literals and quantifiers.

regex_re = re.compile(r'(?P<group>\?P<(\w+)>|(\w+))|(?P<literal>[^()]+)')

def regex(pattern):
    """
    Parser a regex pattern into capture groups and literals.
    """
    yield from regex_re.finditer(pattern)

def collapse_dict(data):
    """
    Collapse similar keys with the same values in a dict.
    """
    # Only works for abc1, abc2, ..., abcN keys for now.
    result = {}

    prefixes = defaultdict(list)
    for key in data:
        key_parts = re.split(r'(\d+)', key.casefold())
        key_parts = [part for part in key_parts if part]
        if len(key_parts) == 2:
            prefix, *_ = key_parts
            prefixes[prefix].append(key)
        else:
            # Save as is.
            result[key] = data[key]

    for prefix, keys in prefixes.items():
        if len(set(data[key] for key in keys)) == 1:
            for key in keys:
                break
            result[prefix] = data[key]
        else:
            for key in keys:
                result[key] = data[key]

    return result
