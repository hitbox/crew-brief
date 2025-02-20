def visit(data, parents=None):
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

def visit_for_dict(data, key_sort=None, parents=None):
    if parents is None:
        parents = tuple()

    if isinstance(data, dict):
        for key in sorted(data, key=key_sort):
            value = data[key]
            yield from visit_for_dict(value, key_sort=key_sort, parents=parents + (key,))
    else:
        yield (parents, data)

def drill(data, keys):
    for key in keys:
        if isinstance(data, list):
            try:
                key = int(key)
                data = data[key]
            except (ValueError, IndexError):
                if all(isinstance(item, dict) and key in item for item in data):
                    data = [item[key] for item in data]
                else:
                    raise KeyError(f'Key "{key}" not found in list items.')
        elif isinstance(data, dict):
            if key in data:
                data = data[key]
            else:
                raise KeyError(f'Key "{key}" not found in dictionary.')
    return data

def try_drill(data, keys, ignore_missing=True):
    try:
        return drill(data, keys)
    except KeyError:
        if not ignore_missing:
            raise

def discover_structure(data, depth=0):
    """
    Recursively explores nested data and prints its structure.
    """
    # Indentation for visualization
    indent = "  " * depth

    if isinstance(data, dict):
        print(f"{indent}Dict with {len(data)} keys:")
        for key, value in data.items():
            print(f"{indent}  Key: {repr(key)} -> ", end="")
            discover_structure(value, depth + 1)
    elif isinstance(data, list):
        print(f"{indent}List with {len(data)} elements:")
        for i, item in enumerate(data[:3]):
            # Show first 3 elements for brevity
            print(f"{indent}  [{i}] -> ", end="")
            discover_structure(item, depth + 1)
        if len(data) > 3:
            print(f"{indent}  ... ({len(data) - 3} more elements)")
    elif isinstance(data, tuple):
        print(f"{indent}Tuple with {len(data)} elements:")
        for i, item in enumerate(data):
            print(f"{indent}  ({i}) -> ", end="")
            discover_structure(item, depth + 1)
    elif isinstance(data, set):
        print(f"{indent}Set with {len(data)} elements:")
        for item in list(data)[:3]:
            # Convert to list to iterate safely
            print(f"{indent}  - ", end="")
            discover_structure(item, depth + 1)
        if len(data) > 3:
            print(f"{indent}  ... ({len(data) - 3} more elements)")
    else:
        print(f"{indent}{type(data).__name__}: {repr(data)}")
