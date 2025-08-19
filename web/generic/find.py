from flask import render_template
from flask import request
from flask.views import View
from wtforms import Field

from web.extension import db

class FindView(View):
    """
    View to find objects.
    """

    def __init__(self, form_class, statement, table, template):
        self.form_class = form_class
        self.statement = statement
        self.table = table
        self.template = template

    def dispatch_request(self, *args, **kwargs):
        form = self.form_class(request.args)
        context = {
            'form': form,
            'table': self.table,
        }

        query = {}
        for field in form:
            if field.__class__.__name__ == 'SubmitField':
                continue

            if field.data['filter']:
                query[field.name] = field.data['value']

        if query:
            statement = self.statement(query)
            pagination = db.paginate(statement)

            context.update({
                'stmt': statement,
                'pagination': pagination,
            })

        context['query'] = query
        return render_template(self.template, **context)
