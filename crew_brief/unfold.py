def _is_dict_val(item):
    return isinstance(item[1], dict)

def unfold_dict(data, sep='.'):
    """
    Flatten nested dicts into a header row and values row. This loses the
    "upper" keys of nested dicts. Nested dicts are sorted to the end.

    Example:
        data = {'a': 1, 'b': 2, 'c': {'k1': 'z'}}
        gen = unfold_dict(data)
        next(gen)  # ('a', 'b', 'c.k1')
        next(gen)  # (1, 2, 'z')
    """
    keys = tuple()
    vals = tuple()

    # Dicts sorted to last.
    items = sorted(data.items(), key=_is_dict_val)

    for key, val in items:
        # If not empty dict.
        if isinstance(val, dict) and val:
            generator = unfold_dict(val)
            keys += tuple(sep.join([key, subkey]) for subkey in next(generator))
            vals += next(generator)
        else:
            keys += (key, )
            vals += (val, )

    yield keys
    yield vals
