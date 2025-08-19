import sqlalchemy as sa

from flask import request
from flask import url_for

def edit_endpoint(model):
    return f'model.{model.__tablename__}.edit'

def table_endpoint(model):
    return f'model.{model.__tablename__}.table'

def instance_endpoint(model):
    return f'model.{model.__tablename__}.instance'

def new_endpoint(model):
    return f'model.{model.__tablename__}.new'

def get_pk_dict(instance):
    mapper = sa.inspect(instance.__class__)
    return {key.name: getattr(instance, key.name) for key in mapper.primary_key}

def url_for_instance(instance):
    return url_for(instance_endpoint(instance.__class__), **get_pk_dict(instance))

def url_for_edit(instance):
    return url_for(edit_endpoint(instance.__class__), **get_pk_dict(instance))

def url_for_new(model):
    return url_for(new_endpoint(model))

def url_for_page(endpoint, page):
    """
    `url_for` that preserves pagination query args.
    """
    args = request.args.to_dict(flat=True)
    args['page'] = page
    return url_for(endpoint, **request.view_args, **args)

def url_for_groupby(table, *attrnames):
    return url_for('groupby.attr', table=table, attrnames='/'.join(attrnames))

def init_app(app):
    app.jinja_env.globals['url_for_edit'] = url_for_edit
    app.jinja_env.globals['url_for_groupby'] = url_for_groupby
    app.jinja_env.globals['url_for_instance'] = url_for_instance
    app.jinja_env.globals['url_for_new'] = url_for_new
    app.jinja_env.globals['url_for_page'] = url_for_page
