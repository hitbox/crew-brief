from flask import Blueprint
from flask import render_template
from flask import url_for

from crew_brief.model import get_models
from htmlkit import Column
from htmlkit import Table

from .model import add_model_views

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

database_objects_table = Table([
    Column(
        '__tablename__',
        label = 'Table',
    ),
])

@admin_bp.route('/')
def index():
    """
    Table listing of database objects and a description.
    """
    rows = []
    for name, model_class in get_models().items():
        rows.append({
            'name': name,
            'description': model_class.__doc__,
            'href': url_for(f'admin.{model_class.__tablename__}.table'),
        })

    context = {
        'table': database_objects_table,
        'models': get_models(),
        'rows': rows,
    }

    return render_template('admin.html', **context)

add_model_views(admin_bp)
