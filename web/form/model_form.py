from collections import OrderedDict

from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.orm import ModelConverter
from wtforms_sqlalchemy.orm import converts
from wtforms_sqlalchemy.orm import model_form as wtfsa_model_form

from web.extension import db

from .converter import CustomModelConverter

class ModelForm(FlaskForm):

    submit = SubmitField('Save')

    def _fields_sort_key(self, name, field):
        # This method and __init__ and intimately dancing.
        if isinstance(field, SubmitField):
            # Sort button/submit fields to end.
            return float('inf')

        elif hasattr(self.model_class, field.name):
            model_attr = getattr(self.model_class, field.name)
            if hasattr(model_attr, 'info') and 'field_order' in model_attr.info:
                return model_attr.info['field_order']

        return list(self._fields.keys()).index(name)

    def __init__(self, *args, model_class=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = model_class
        self._sort_fields(lambda item: self._fields_sort_key(*item))

    def _sort_fields(self, sortkey):
        self._fields = OrderedDict(sorted(self._fields.items(), key=sortkey))

    @property
    def _input_fields(self):
        for field in self:
            if field.type not in ('CSRFTokenField', 'SubmitField'):
                yield field

    @property
    def _button_fields(self):
        for field in self:
            if field.type in ('SubmitField', ):
                yield field


def exclude_properties(model):
    exclude = []
    for key in dir(model):
        attr = getattr(model, key)
        if hasattr(attr, 'info') and 'hidden' in attr.info:
            exclude.append(key)
    return exclude

def model_form(model, **kwargs):
    kwargs.setdefault('base_class', ModelForm)
    kwargs.setdefault('db_session', db.session)
    kwargs.setdefault('exclude', exclude_properties(model))
    kwargs.setdefault('converter', CustomModelConverter())

    form_class = wtfsa_model_form(model, **kwargs)
    return form_class
