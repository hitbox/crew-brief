from copy import deepcopy

from flask import render_template
from flask.views import View

from crew_brief.util import instance_items
from web.extension import db

class InstanceView(View):

    def __init__(self, model_class, definition_list, template, get_context):
        self.model_class = model_class
        self.definition_list = definition_list
        self.template = template
        self.get_context = get_context

    def dispatch_request(self, **identity):
        instance = db.session.get(self.model_class, identity)

        items = instance_items(instance)

        context = {
            'instance': instance,
            'items': items,
            'definition_list': self.definition_list,
        }
        context = self.get_context(context)

        return render_template(self.template, **context)
