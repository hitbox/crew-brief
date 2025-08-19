from flask import Flask
from flask import current_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from . import converter
from . import endpoint
from . import extension
from . import filters
from . import view

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('CREW_BRIEF_WEB_CONFIG')

    @app.context_processor
    def inject():
        """
        Injection for templates.
        """
        dict_ = current_app.config.get('INJECT', {})
        dict_.setdefault('js_config', current_app.config.get('JS_INJECT', {}))
        dict_.setdefault('current_app', current_app)
        return dict_

    @app.template_filter('as_list')
    def as_list(value):
        """
        Template filter to ensure a list. some_var|as_list -> always a list.
        """
        if not isinstance(value, (list, set, tuple)):
            value = [value]
        return value

    converter.init_app(app)
    endpoint.init_app(app)
    extension.init_app(app)
    filters.init_app(app)
    view.init_app(app)

    if 'APP_URL_PREFIX' in app.config:
        url_prefix = app.config['APP_URL_PREFIX'].rstrip('/')
        # Prefix all client side. Wait until after extensions, some config
        # settings might be filled out by them.
        app.config['SESSION_COOKIE_PATH'] = url_prefix
        # Prefix all routes.
        app.wsgi_app = DispatcherMiddleware(
            Flask('empty'),
            {
                url_prefix: app.wsgi_app,
            },
        )

    return app
