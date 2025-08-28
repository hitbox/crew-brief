from flask import Flask
from flask import current_app

from . import context_processor
from . import converter
from . import endpoint
from . import extension
from . import filters
from . import prefix_middleware
from . import template_filter
from . import view

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_envvar('CREW_BRIEF_WEB_CONFIG')

    context_processor.init_app(app)
    converter.init_app(app)
    endpoint.init_app(app)
    extension.init_app(app)
    filters.init_app(app)
    prefix_middleware.init_app(app)
    template_filter.init_app(app)
    view.init_app(app)

    return app
