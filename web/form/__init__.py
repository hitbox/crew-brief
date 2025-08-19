from crew_brief.model import get_models

from .args import model_form_args
from .model_form import model_form
from .query import model_find_form
from .query import model_query_form

_models = get_models()

by_name = {
    name: model_form(model, **model_form_args.get(name, {}))
    for name, model in _models.items()
}

sort_form_by_name = {name: model_query_form(model) for name, model in _models.items()}
