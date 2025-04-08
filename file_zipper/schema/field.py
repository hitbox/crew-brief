import datetime

import marshmallow as mm

class DateTimeTransformer:

    def __init__(self, load_format, dump_format='%Y-%m-%dT%H:%M:%S.%f%z'):
        self.load_format = load_format
        self.dump_format = dump_format

    def load(self, value):
        return datetime.datetime.strptime(value, self.load_format)

    def dump(self, value):
        return value.strftime(self.dump_format)


class DateTransformer(DateTimeTransformer):

    def __init__(self, load_format, dump_format='%Y-%m-%d'):
        super().__init__(load_format, dump_format)


    def load(self, value):
        return datetime.datetime.strptime(value, self.load_format).date()


class TransformField(mm.fields.Field):
    """
    Load data one way and dump another.
    """

    def __init__(self, load_transform, dump_transform, *args, **kwargs):
        self.load_transform = load_transform
        self.dump_transform = dump_transform
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        try:
            return self.dump_transform(value)
        except Exception as e:
            raise mm.ValidationError(f'Error serializing field: {e}')

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return self.load_transform(value)
        except Exception as e:
            raise mm.ValidationError(f'Error serializing field: {e}')


class TransformDateTimeField(TransformField):
    """
    Transform between load and dump for datetime values.
    """

    def __init__(self, load_format, *args, dump_format='%Y-%m-%dT%H:%M:%S.%f%z', **kwargs):
        transformer = DateTimeTransformer(load_format, dump_format)
        kwargs.setdefault('load_transform', transformer.load)
        kwargs.setdefault('dump_transform', transformer.dump)
        super().__init__(*args, **kwargs)


class TransformDateField(TransformField):
    """
    Transform between load and dump for date values.
    """

    def __init__(self, load_format, *args, dump_format='%Y-%m-%d', **kwargs):
        transformer = DateTransformer(load_format, dump_format)
        kwargs.setdefault('load_transform', transformer.load)
        kwargs.setdefault('dump_transform', transformer.dump)
        super().__init__(*args, **kwargs)
