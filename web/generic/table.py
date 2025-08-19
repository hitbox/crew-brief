from copy import deepcopy

import sqlalchemy as sa

from flask import render_template
from flask.views import View

from web.extension import db

class TableView(View):
    """
    Class-based view to list objects in a table.
    """

    def __init__(
        self,
        model_class,
        table,
        template,
        get_statement,
        get_context,
        breadcrumbs_factory = None,
        include_statement = False,
    ):
        self.model_class = model_class
        self.table = table
        self.template = template
        self.breadcrumbs_factory = breadcrumbs_factory
        self.get_statement = get_statement
        self.get_context = get_context
        self.include_statement = include_statement

    def dispatch_request(self, *args, **kwargs):
        stmt = self.get_statement(self.model_class)
        pagination = db.paginate(stmt)

        context = {
            'table': self.table,
            'pagination': pagination,
            'model_class': self.model_class,
        }
        if self.include_statement:
            context['stmt'] = stmt
        context = self.get_context(context)

        return render_template(self.template, **context)
