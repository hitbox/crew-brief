from wtforms.validators import InputRequired
from wtforms_sqlalchemy.orm import ModelConverter
from wtforms_sqlalchemy.orm import converts

class CustomModelConverter(ModelConverter):
    """
    Custom ModelConverter to allow unchecked boolean fields.
    """

    @converts('Boolean')
    def conv_Boolean(self, field_args, **kwargs):
        column = kwargs.get('column')
        if column is not None:
            if column.nullable:
                field_args['validators'] = [
                    validator for validator in field_args['validators']
                    if not isinstance(validator, InputRequired)
                ]
        return super().conv_Boolean(field_args, **kwargs)

    #@converts('NullType')
    #def conv_NullType(self, field_args, **kwargs):
    #    breakpoint()
