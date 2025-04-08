import sqlalchemy as sa

from flask import render_template
from flask.views import View

from file_zipper.web.extension import db

from .model_attrs import InstanceAttrs

class ObjectView(View):
    """
    View on an instance of a model.
    """

    def __init__(
        self,
        model_class,
        template = None,
        instance_endpoint = None,
        list_endpoint = None,
        title = None,
        subtitle = None,
        description = None,
    ):
        self.model_class = model_class
        self.template = template
        self.instance_endpoint = instance_endpoint
        self.list_endpoint = list_endpoint
        self.title = title
        self.subtitle = subtitle
        self.description = description

    def get_template(self):
        template = self.template
        if template is None:
            template = 'object.html'
        return template

    def dispatch_request(self, **ident):
        instance = db.session.get(self.model_class, ident)
        inspector = sa.inspect(instance)
        model_attrs = InstanceAttrs(
            inspector,
            instance_endpoint = self.instance_endpoint,
            list_endpoint = self.list_endpoint,
        )
        context = {
            'description': self.description,
            'instance': instance,
            'model_attrs': model_attrs,
            'model_class': self.model_class,
            'subtitle': self.subtitle,
            'title': self.title,
        }
        return render_template(self.get_template(), **context)
