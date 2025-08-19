import datetime

from werkzeug.routing import BaseConverter

class BooleanConverter(BaseConverter):

    def to_python(self, value):
        return bool(value == str(True))

    def to_url(self, value):
        return str(value)


class DateConverter(BaseConverter):

    def to_python(self, value):
        return datetime.date.fromisoformat(value)

    def to_url(self, value):
        return value.isoformat()


class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split(',')

    def to_url(self, values):
        return ','.join(map(str, values))


def init_app(app):
    app.url_map.converters['bool'] = BooleanConverter
    app.url_map.converters['date'] = DateConverter
    app.url_map.converters['list'] = ListConverter
