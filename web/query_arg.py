import operator

import sqlalchemy as sa

from markupsafe import Markup

from flask import request

def get_column_type(attr):
    try:
        column = attr.property.columns[0]
        return column.type.python_type
    except:
        return None

def parse_where(args):
    filters = {}
    for full_key, value in args.items():
        if not (full_key.startswith('where[') and full_key.endswith(']')):
            continue

        # Strip "where[" and "]"
        inner = full_key[6:-1]
        if '][' in inner:
            field, op = inner.split('][', 1)
        else:
            field, op = inner, 'eq'

        filters.setdefault(field, []).append((op, value))

    return filters

def parse_args_for_criteria(model):
    criteria = []
    filters = parse_where(request.args)
    for field, op_value_list in filters.items():
        attr = getattr(model, field, None)
        if attr is None:
            continue
        for op, value in op_value_list:
            if op == 'in':
                op = lambda a, b: a in b
            else:
                op = getattr(operator, op, None)

            if op is None:
                continue

            type_ = get_column_type(attr)
            if type_ is not None:
                if type_ is bool:
                    type_ = lambda value: bool(int(value))

            if ',' in value:
                value = tuple(map(type_, value.split(',')))
            else:
                value = type_(value)

            criteria.append(op(attr, value))
    return criteria

def statement_for_model(model):
    stmt = sa.select(model)
    for crit in parse_args_for_criteria(model):
        stmt = stmt.where(crit)

    for field in request.args.getlist('sort'):
        desc = field.startswith('-')
        if desc:
            field = field[1:]
        attr = getattr(model, field, None)
        if attr is None:
            continue
        if desc:
            attr = attr.desc()
        stmt = stmt.order_by(attr)

    return stmt

def page_title_for_model(model):
    html = [
        '<h2>Files successfully parsed for leg identifiers.</h2>',
    ]
    return Markup(''.join(html))

def is_true_string(string):
    return string.lower() in ('true', '1', 'yes', 'on')
