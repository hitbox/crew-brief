import sqlalchemy as sa

from flask import Blueprint

from crew_brief.model import Airline
from crew_brief.model import get_models
from crew_brief.model import LegFile
from web.breadcrumbs import build_breadcrumbs
from web.form import model_find_form
from web.generic import FindView
from web.table import model_tables

find_bp = Blueprint('find', __name__, url_prefix='/find')

@find_bp.context_processor
def context_processor():
    return {'breadcrumbs': build_breadcrumbs()}

def add_for_model(model):
    find_bp.add_url_rule(
        f'/{model.__tablename__}',
        view_func = FindView.as_view(
            model.__tablename__,
            form_class = model_find_form(model),
            statement = lambda query: sa.select(model).filter_by(**query),
            table = model_tables[model],
            template = 'find.html',
        ),
    )

for model in get_models().values():
    add_for_model(model)
