from flask import Blueprint
from markupsafe import Markup

from crew_brief.model import get_models
from crew_brief.util import url_rule_for_model
from htmlkit import Column
from htmlkit import DefinitionList
from htmlkit import model_html_table
from web import form
from web.context import InstanceContext
from web.context import TableContext
from web.endpoint import url_for_edit
from web.generic import EditView
from web.generic import InstanceView
from web.generic import NewView
from web.generic import TableView
from web.instance import model_instance_args
from web.query_arg import statement_for_model
from web.table import model_table_args

edit_column = Column(
    label = 'Admin',
    formatter = lambda inst, val:
        Markup(
            f'<a'
            f' class="btn btn-primary btn-sm" role="button"'
            f' href="{url_for_edit(inst)}">Edit</a>'
        )
)

def add_table_listing_blueprint(name, model, parent_bp, include_edit_column=False):
    """
    Add route to table listing for a model.
    """
    table_args = model_table_args.get(name, {})
    table_args.setdefault('include_relationships', True)
    table = model_html_table(model, **table_args)

    if include_edit_column:
        # Insert a column for links to edit objects.
        table.columns.insert(0, edit_column)

    table_context = TableContext(model)

    table_view_func = TableView.as_view(
        'table',
        model_class = model,
        # HTML table renderer for model.
        table = table,
        template = 'table.html',
        get_statement = statement_for_model,
        get_context = table_context.get_context,
    )

    # Add model table view as blueprint for name spacing.
    parent_bp.add_url_rule(f'/{model.__tablename__}/', view_func=table_view_func)

def add_instance_blueprint(name, model, parent_bp):
    """
    Add route to a view of an instance.
    """
    model_args = model_instance_args.get(name, {})
    model_args.setdefault('include_relationships', True)

    instance_context = InstanceContext(model)

    view_func = InstanceView.as_view(
        'instance',
        model_class = model,
        definition_list = DefinitionList.from_model(model, **model_args),
        template = 'instance.html',
        get_context = instance_context.get_context,
    )
    primary_key_rules = '/'.join(url_rule_for_model(model))
    rule = f'/{model.__tablename__}/' + primary_key_rules
    parent_bp.add_url_rule(rule, view_func=view_func)

def add_new_instance_blueprint(name, model, parent_bp):
    """
    New instance of model class view.
    """
    view_func = NewView.as_view(
        'new',
        form_class = form.by_name[name],
        model_class = model,
        template = 'edit.html',
        get_context = lambda context: context,
    )
    parent_bp.add_url_rule(f'/new/{model.__tablename__}', view_func=view_func)

def add_edit_instance_blueprint(name, model, parent_bp):
    """
    Edit an instance of model class view.
    """
    form_class = form.by_name[name]

    view_func = EditView.as_view(
        'edit',
        form_class = form_class,
        model_class = model,
        template = 'edit.html',
        page_title = Markup(f'<h2>{name}</h2>'),
    )
    primary_key_rules = '/'.join(url_rule_for_model(model))
    rule = f'/edit/{model.__tablename__}/' + primary_key_rules
    parent_bp.add_url_rule(rule, view_func=view_func)

def blueprint_name(model):
    return f'{model.__tablename__}'

def add_model_views(app_or_blueprint):
    """
    Register all database models as blueprints to argument.
    """
    for model_name, model in get_models().items():
        model_blueprint = Blueprint(blueprint_name(model), __name__)

        app_or_blueprint.register_blueprint(model_blueprint)

        add_table_listing_blueprint(
            model_name,
            model,
            model_blueprint,
            include_edit_column = True,
        )
        add_new_instance_blueprint(model_name, model, model_blueprint)
        add_instance_blueprint(model_name, model, model_blueprint)
        add_edit_instance_blueprint(model_name, model, model_blueprint)
