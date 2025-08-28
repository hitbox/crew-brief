import calendar
import importlib
import re

import sqlalchemy as sa

from flask import url_for
from markupsafe import Markup
from sqlalchemy.ext.hybrid import hybrid_property

class Batch:
    """
    Batch commit work.
    """

    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.work = []

    def append(self, session, item):
        self.work.append(item)
        if len(self.work) % self.batch_size == 0:
            session.commit()
            self.work.clear()

    def finalize(self, session):
        if self.work:
            session.commit()
            self.work.clear()


def invert_dict(d, strict=False):
    """
    Invert keys and values for dict d. If strict, raise for duplicate
    value-keys.
    """
    inverted = {}
    for key, val in d.items():
        if strict and val in inverted:
            raise ValueError(f'Duplicate key for value {val}')
        inverted[val] = key
    return inverted

def is_one(*args, null=None):
    """
    Exactly one arg in args is not in the null set.
    """
    if not isinstance(null, (list, set, tuple)):
        null = [null]
    else:
        null = list(set(null))
    return sum(arg not in null for arg in args) == 1

def get_info_dict(attr):
    return getattr(attr, 'info', {})

def get_is_hidden(attr):
    return get_info_dict(attr).get('hidden', False)

def model_attributes(
    model,
    include_pk = False,
    include_fk = False,
    include_relationships = False,
    ignore_private = False,
):
    """
    Natural attribute order optionally sorted by info dict.
    """
    # get attribute names from model that should be shown
    keys = []

    for name, attr in model.__dict__.items():
        if ignore_private and name.startswith('_'):
            continue
        if isinstance(attr, property):
            keys.append(name)
        elif isinstance(attr, sa.orm.attributes.InstrumentedAttribute):
            is_hidden = get_is_hidden(attr)
            if isinstance(attr.property, sa.orm.ColumnProperty):
                colprop = attr.property
                column = colprop.columns[0]
                is_pk = column.primary_key
                is_fk = bool(column.foreign_keys)
                if (include_pk or not is_pk) and (include_fk or not is_fk) and not is_hidden:
                    keys.append(name)
            elif isinstance(attr.property, sa.orm.RelationshipProperty):
                if include_relationships and not is_hidden:
                    keys.append(name)
    return keys

def instance_items(instance):
    """
    Return tuples of (header_value, instance_value) for rendering instancs as
    html definition lists.
    """
    model = instance.__class__
    keys = model_attributes(model, include_relationships=True)
    items = tuple(
        (get_header_value(model, key), getattr(instance, key))
        for key in keys
    )
    return items

def _converter_for_column(column):
    col_type = column.type
    if isinstance(col_type, sa.Integer):
        return 'int'
    elif isinstance(col_type, sa.String):
        return 'string'
    elif isinstance(col_type, sa.Float):
        return 'float'
    else:
        raise TypeError(f'{col_type} not supported for url rule.')

def url_rule_for_model(model):
    mapper = sa.inspect(model)
    parts = []
    for col in mapper.primary_key:
        converter = _converter_for_column(col)
        parts.append(f'<{converter}:{col.name}>')
    return parts

def instance_endpoint(instance):
    # NOTE: crew_brief.web.view.model blueprints produce this namespaced name.
    return f'model.{instance.__class__.__tablename__}.instance'

def get_value_for_instance(instance, attr):
    """
    Simply get the value from an instances attribute, or if a special attribute
    is given, it is used.
    """
    # TODO
    return getattr(instance, attr)

def get_header_value(model_class, attr):
    attribute = getattr(model_class, attr)
    info = getattr(attribute, 'info', {})
    if info and 'label' in info:
        text = info['label']
    else:
        text = attr

    if hasattr(attribute, 'doc') and attribute.doc:
        doc = attribute.doc
        return Markup(f'<span title="{doc}">{text}</span>')
    else:
        return text

def url_for_instance(obj):
    """
    Return the url for an instance model.
    """
    state = sa.inspect(obj)
    endpoint = f'model.{obj.__class__.__tablename__}.instance'
    rule_values = {col.key: getattr(obj, col.key) for col in state.mapper.primary_key}
    return url_for(endpoint, **rule_values)


_CAMEL_SPLITTER = re.compile(
    r'''
    (?<=[A-Za-z])      # preceded by a letter
    (?=                # followed by…
        [A-Z][a-z] |   #    Upper+lower   e.g. "Walk"
        [0-9] |        #  or digit        e.g. "IPv6"
        (?=[A-Z][A-Z]) #  or next is a run of capitals (keep acronym intact)
    )
    ''',
    re.VERBOSE,
)

def humanize_class_name(name):
    """
    Convert 'OSWalk'   -> 'OS Walk'
            'LegIdentifier' -> 'Leg Identifier'
            'HTMLParser'    -> 'HTML Parser'
            'IPv6Address'   -> 'IPv6 Address'
    Accepts a *class object* or a *string*.
    """
    if not isinstance(name, str):
        name = name.__name__

    parts = _CAMEL_SPLITTER.split(name)
    # Preserve all‑caps acronyms verbatim, title‑case the rest
    for i, part in enumerate(parts):
        if not part.isupper():
            parts[i] = part.capitalize()
    return " ".join(parts)

def load_from_path(dotted_path):
    """
    Load object from dotted path string.
    """
    module_path, obj_name = dotted_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, obj_name)

def abbreviate(text, max_length=40, ellipsis='...', from_end=False):
    if len(text) <= max_length:
        return text

    slice_length = max_length - len(ellipsis)
    if from_end:
        return ellipsis + text[-slice_length:]
    else:
        return text[:slice_length] + ellipsis

def split_at(text, index):
    return text[:index], text[index:]

def is_foreign_key(attr):
    if isinstance(attr, sa.orm.ColumnProperty):
        for column in attr.columns:
            if column.foreign_keys:
                return True
    return False

def hybrid_date_part(srcname, part):
    """
    Add property and expression for getting the date part of a column.
    """
    def getter(self):
        return getattr(getattr(self, srcname), part, None)

    def expression(cls):
        return sa.func.cast(sa.func.extract(part, getattr(cls, srcname)), sa.Integer)

    return hybrid_property(getter).expression(expression)

def escape_for_configparser(s):
    """
    Escape string to avoid configparser interpolation.
    """
    # This may need more escaping.
    return s.replace('%', '%%')
