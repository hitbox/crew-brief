from copy import deepcopy

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.views import View

from web.extension import db

class NewView(View):
    """
    New instance edit view.
    """

    methods = ['GET', 'POST']

    def __init__(self, form_class, model_class, template, get_context):
        self.form_class = form_class
        self.model_class = model_class
        self.template = template
        self.get_context = get_context

    def dispatch_request(self, *args, **kwargs):
        """
        """
        form = self.form_class()

        if form.validate_on_submit():
            new_instance = self.model_class()
            db.session.add(new_instance)
            form.populate_obj(new_instance)
            db.session.commit()
            return redirect(url_for(request.endpoint, **request.view_args))

        context = {'form': form}
        context = self.get_context(context)

        return render_template(self.template, **context)


class EditView(View):
    """
    Edit objects with a form.
    """

    methods = ['GET', 'POST']

    def __init__(self, form_class, model_class, template, breadcrumbs_factory=None, **context):
        self.form_class = form_class
        self.model_class = model_class
        self.template = template
        self.breadcrumbs_factory = breadcrumbs_factory
        self.context = context

    def dispatch_request(self, *args, **identity):
        instance = db.session.get(self.model_class, identity)
        form = self.form_class(obj=instance, model_class=self.model_class)

        if form.validate_on_submit():
            form.populate_obj(instance)
            db.session.commit()
            flash('Updated', 'info')
            return redirect(url_for(request.endpoint, **request.view_args))

        context = deepcopy(self.context)
        context.update({
            'instance': instance,
            'form': form,
        })

        if callable(self.breadcrumbs_factory):
            context['breadcrumbs'] = self.breadcrumbs_factory()

        return render_template(self.template, **context)
