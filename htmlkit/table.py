from markupsafe import Markup
from sqlalchemy.orm import RelationshipProperty

from crew_brief.util import model_attributes
from htmlkit.core import render_tag
from htmlkit.core import unordered_list

class Column:
    """
    Column of an html table. Holds the attribute name (key) that should be
    available on instance of the model. An optional label for the <th>. And
    optional formatter, for creating the values that show in the <td>'s.
    """

    def __init__(self, key=None, label=None, formatter=None, attrs=None):
        # key is allowed to be None to avoid expensive attribute access.
        self.key = key
        self.label = label
        if self.key is None and self.label is None:
            raise ValueError(f'key or label must be defined.')
        self.formatter = formatter
        self.attrs = attrs

    def render_th(self):
        return Markup(self.label or self.key)

    def render_td(self, obj):
        if self.key is not None:
            value = getattr(obj, self.key)
        else:
            value = self.label

        if self.formatter:
            value = self.formatter(obj, value)

        return Markup(value)


class Table:
    """
    HTML Table that basically holds the columns and provides way to iterate them.
    """

    def __init__(self, columns):
        self.columns = columns

    def render_thead(self):
        html = []
        for column in self.columns:
            html.append(column.render_th())
        return Markup(''.join(html))

    def render_tr(self, obj):
        html = []
        for column in self.columns:
            html.append(column.render_td(obj))
        return Markup(''.join(html))


def get_formatter(attr):
    """
    Special formatter for relationship attribute/properties.
    """
    if hasattr(attr, 'property'):
        prop = attr.property
        if isinstance(prop, RelationshipProperty):
            if prop.uselist:
                def formatter(instance, value):
                    return unordered_list(map(Markup, value))
                return formatter

def update_for_info(attr, attrname, kwargs, field_args):
    info = getattr(attr, 'info', {})
    if 'label' in info:
        kwargs['label'] = info['label']

    if 'formatter' in info:
        kwargs['formatter'] = info['formatter']

    if attrname in field_args:
        kwargs.update(field_args[attrname])

def model_html_table(
    model,
    include_relationships = True,
    field_args = None,
    only = None,
    sort_key = None,
):
    """
    Create HTML Table object from database model.
    """
    # TODO
    # - Merge-refactor with DefinitionList.from_model
    if field_args is None:
        field_args = {}
    columns = []
    attrs = model_attributes(model, include_relationships=include_relationships)
    for attrname in attrs:
        if only and attrname not in only:
            continue
        attr = getattr(model, attrname)

        # Construct formatter if attribute is a relationship.
        formatter = get_formatter(attr)

        kwargs = {'key': attrname}
        update_for_info(attr, attrname, kwargs, field_args)

        table_column = Column(**kwargs)
        columns.append(table_column)

    # Sort the column if key given.
    if sort_key is not None:
        columns.sort(key=sort_key)

    html_table = Table(columns)
    return html_table
