import sqlalchemy as sa

from flask import Blueprint
from flask import render_template
from flask import url_for
from markupsafe import Markup

from crew_brief.model import LegFile
from crew_brief.model import get_models
from crew_brief.statistics import file_stats
from htmlkit import Column
from htmlkit import Table
from web.breadcrumbs import build_breadcrumbs
from web.extension import db
from web.table import stats_table

core_bp = Blueprint('core', __name__)

@core_bp.context_processor
def context_processor():
    return {
        'breadcrumbs': build_breadcrumbs(),
    }

@core_bp.route('/')
def root():
    """
    Root view. List of objects to browse.
    """
    database_objects = []
    for class_name, model in get_models().items():
        database_objects.append({
            'href': url_for(f'admin.{model.__tablename__}.table'),
            'text': class_name,
        })

    context = {
        'database_objects': database_objects,
        'stats': file_stats(db.session),
        'stats_table': stats_table,
    }
    return render_template('root.html', **context)
