import sqlalchemy as sa

from flask import render_template
from flask.views import View

from file_zipper.web.extension import db

class ListView(View):
    """
    List of model objects pluggable view.
    """

    def __init__(
        self,
        model_class,
        template = None,
        statement = None,
        endpoint = None,
        title = None,
        subtitle = None,
        description = None,
    ):
        self.model_class = model_class
        self.template = template
        self.statement = statement
        self.endpoint = endpoint
        self.title = title
        self.subtitle = subtitle
        self.description = description

    def get_template(self):
        template = self.template
        if template is None:
            template = 'list.html'
        return template

    def get_statement(self):
        statement = self.statement
        if statement is None:
            statement = db.select(self.model_class)
        return statement

    def dispatch_request(self):
        statement = self.get_statement()
        objects = db.paginate(statement)
        inspector = sa.inspect(self.model_class)
        context = {
            'objects': objects,
            'model_class': self.model_class,
            'inspector': inspector,
            'endpoint': self.endpoint,
            'title': self.title,
            'subtitle': self.subtitle,
            'description': self.description,
        }
        return render_template(self.get_template(), **context)
