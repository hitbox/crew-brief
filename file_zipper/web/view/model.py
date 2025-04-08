import code

import click
import sqlalchemy as sa

from flask import Blueprint
from flask import request
from flask import url_for

from file_zipper.model import Path
from file_zipper.web.extension import db
from file_zipper.web.model import model_list
from file_zipper.web.model import statements
from file_zipper.web.pluggable import ListView
from file_zipper.web.pluggable import ObjectView
from file_zipper.web.pluggable import SendFileView
from file_zipper.web.url import model_url_rule

model_blueprint = Blueprint('model', __name__, url_prefix='/model')

def name_for_model(model_class):
    return model_class.__table__.name

def path_instance_from_request():
    return db.session.get(Path, request.view_args['id'])

def add_send_file_view(model_class, blueprint, url, name):
    """
    Add endpoints for objects that want to send files.
    """
    # Endpoint to send file.
    blueprint.add_url_rule(
        url,
        view_func = SendFileView.as_view(
            name = name,
            mimetype = lambda: path_instance_from_request().file_type.mime_type,
            as_attachment = False,
        ),
    )

def instance_endpoint(instance):
    """
    Build url for instance to its object view.
    """
    view = f'model.{instance.__table__.name}.instance'
    return url_for(view, id=instance.id)

def list_endpoint(model_class):
    view = f'model.{model_class.__table__.name}.list'
    return url_for(view)

def add_list_view(model_class, blueprint):
    """
    Add url rule for showing list of objects.
    """
    blueprint.add_url_rule(
        f'/{name_for_model(model_class)}',
        view_func = ListView.as_view(
            name = 'list',
            model_class = model_class,
            statement = statements.get(model_class),
            title = f'{model_class.__name__} Objects',
            description = model_class.__doc__,
            endpoint = '.instance',
        ),
    )

def add_object_view(model_class, blueprint):
    """
    Add view of a single object.
    """
    url = model_url_rule(model_class)

    template = None
    if model_class is Path:
        template = 'path_object.html'

    # Add view to send file for Path objects.
    if model_class is Path:
        add_send_file_view(
            model_class,
            blueprint,
            f'{url}/file/<filename>',
            'send_file',
        )

    blueprint.add_url_rule(
        url,
        view_func = ObjectView.as_view(
            name = 'instance',
            model_class = model_class,
            template = template,
            instance_endpoint = instance_endpoint,
            list_endpoint = list_endpoint,
            title = f'{model_class.__name__} Instance',
            description = model_class.__doc__,
        ),
    )

def add_command_line(model_class, blueprint):
    """
    Add cli for a shell with an inspector for this model.
    """

    @blueprint.cli.command()
    def inspect():
        inspector = sa.inspect(model_class)
        local = {
            'inspector': inspector,
        }
        code.interact(local=local)

def add_blueprint_for_model(model_class):
    name = name_for_model(model_class)
    class_blueprint = Blueprint(name, __name__)
    add_list_view(model_class, class_blueprint)
    add_object_view(model_class, class_blueprint)
    add_command_line(model_class, class_blueprint)
    return class_blueprint

# Add a list and object view for models.
for model_class in model_list:
    class_blueprint = add_blueprint_for_model(model_class)
    model_blueprint.register_blueprint(class_blueprint)
