"""
Functions for recursively visiting data.
"""

def visit(data, parents=None):
    """
    Recursively generate tuples (parents, data).
    """
    if parents is None:
        parents = tuple()

    if isinstance(data, dict):
        for key, value in data.items():
            yield from visit(value, parents + (key,))
    elif isinstance(data, (list, tuple)):
        for index, value in enumerate(data):
            yield from visit(value, parents + (index, ))
    else:
        yield (parents, data)

def drill(data, keys):
    """
    Descend into data structures with a list of keys.
    """
    for key in keys:
        if isinstance(data, list):
            try:
                key = int(key)
                data = data[key]
            except (ValueError, IndexError) as exc:
                if all(isinstance(item, dict) and key in item for item in data):
                    data = [item[key] for item in data]
                else:
                    raise KeyError(f'Key "{key}" not found in list items.') from exc
        elif isinstance(data, dict):
            if key in data:
                data = data[key]
            else:
                raise KeyError(f'Key "{key}" not found in dictionary.')
    return data

def try_drill(data, keys, ignore_missing=True):
    """
    Like drill with option to ignore missing keys.
    """
    try:
        return drill(data, keys)
    except KeyError:
        if not ignore_missing:
            raise
    return None
