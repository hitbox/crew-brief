import sqlalchemy as sa

from flask import Blueprint
from flask import render_template
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
    model_names = list(get_models().items())

    total_files = db.session.scalar(sa.select(sa.func.count()).select_from(LegFile))

    unparsed_count = db.session.scalar(
        sa.select(sa.func.count())
        .select_from(LegFile)
        .where(LegFile.leg_identifier_id == None)
    )

    context = {
        'model_names': model_names,
        'stats': file_stats(db.session),
        'stats_table': stats_table,
    }
    return render_template('root.html', **context)
