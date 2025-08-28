import sqlalchemy as sa

from wtforms import BooleanField
from wtforms import Form
from wtforms import FormField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from crew_brief.util import is_foreign_key
from web.attribute_sort import AttributeSort
from web.extension import db

from .field import DynamicSelectField

class SafeType:
    """
    Callable to intercept common invalid values for a function.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, value):
        if value is None:
            return None
        if value == 'None':
            return None
        return self.func(value)


def attr_filter_field(model, attr, base_class=Form, type_name=None):
    if type_name is None:
        type_name = f'{attr.key}FilterField'

    value_field = StringField()

    if isinstance(attr, sa.orm.RelationshipProperty):
        value_field = QuerySelectMultipleField(
            query_factory = lambda: db.session.scalars(db.select(attr.mapper.class_))
        )
    elif isinstance(attr, sa.orm.ColumnProperty):
        column = attr.columns[0]

        if not isinstance(column.type, sa.DateTime):
            coerce = SafeType(column.type.python_type)
        else:
            coerce = str

        value_field = DynamicSelectField(
            query_factory = lambda: db.session.scalars(db.select(column)),
            coerce = coerce,
        )

    field_dict = {
        'filter': BooleanField(),
        'value': value_field,
    }

    return type(type_name, (base_class, ), field_dict)

def model_find_form(
    model,
    exclude_pk = True,
    exclude_fk = True,
    type_name = None,
    base_class = Form,
):
    if type_name is None:
        type_name = f'Find{model.__name__}Form'

    mapper = sa.inspect(model)
    field_dict = {}
    for attr in mapper.attrs:
        if attr in mapper.primary_key and exclude_pk:
            continue
        if is_foreign_key(attr) and exclude_fk:
            continue
        field_dict[attr.key] = FormField(attr_filter_field(model, attr))

    field_dict['find'] = SubmitField()
    return type(type_name, (base_class, ), field_dict)

def model_query_form(
    model,
    db_session = None,
    base_class = Form,
    type_name = None,
    include_pk = False,
    include_fk = False,
):
    """
    Make a query form from a database model with attributes suffixed for
    sorting and filtering.
    """
    if type_name is None:
        type_name = f'Sort{model.__name__}Form'

    field_dict = {}
    for attrname in dir(model):
        if not attrname.startswith('_'):
            attr = getattr(model, attrname)

            field_dict[attrname + '_sort'] = SelectField(
                choices = [member.choice_item for member in AttributeSort],
            )

            field_dict[attrname + '_filter'] = StringField()

    return type(type_name, (base_class, ), field_dict)

def statement_for_form(model, query_form=None, suffixes=None):
    stmt = sa.select(model)
    if suffixes:
        for suffix in suffixes:
            for attrname in dir(model):
                if attrname.startswith('_'):
                    continue
                if query_form:
                    field = getattr(query_form, attrname + suffix, None)
                    if field and field.data:
                        if suffix == '_sort':
                            attr = getattr(model, attrname)

                            if attrname in mapper.relationships:
                                # Add join for relationship
                                stmt = stmt.join(attr)

                                # relation('Target') class
                                order_attr = attr.mapper.class_.name
                            else:
                                order_attr = attr

                            if field.data == AttributeSort.descending.value:
                                stmt = stmt.order_by(sa.desc(order_attr))
                            else:
                                stmt = stmt.order_by(order_attr)
    return stmt
