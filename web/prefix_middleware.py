from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

def init_app(app):
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

