from copy import deepcopy

import sqlalchemy as sa

from flask import render_template
from flask.views import View

from web.extension import db

class AttributeView(View):
    """
    List a database object and a paginated view of one of it's attributes.
    """

    def __init__(self, model_class, table, attribute, template, **context):
        self.model_class = model_class
        self.table = table
        self.attribute = attribute
        self.template = template
        self.context = context

    def dispatch_request(self, *args, **kwargs):
        instance = db.session.get(self.model_class, kwargs)

        rel = getattr(self.model_class, self.attribute).property
        related_model = rel.mapper.class_

        # This assumes a simple relationship with a single foreign key.
        foreign_key = next(iter(rel.local_remote_pairs))[0]
        stmt = sa.select(related_model).join(self.model_class).where(foreign_key == instance.id)
        pagination = db.paginate(stmt)

        context = deepcopy(self.context)
        context.update({
            'instance': instance,
            'stmt': stmt,
            'table': self.table,
            'pagination': pagination,
        })

        return render_template(self.template, **context)
