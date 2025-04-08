from flask import Flask

from file_zipper.sql_function import register_functions
from file_zipper.web import model
from file_zipper.web import template_filter
from file_zipper.web.extension import db
from file_zipper.web.view import model_blueprint
from file_zipper.web.view import query_blueprint
from file_zipper.web.view import root_blueprint

def create_app():
    """
    Create web app interface for file_zipper.
    """
    app = Flask(__name__)
    app.config.from_envvar('FILE_ZIPPER_CONFIG')

    db.init_app(app)

    with app.app_context():
        db.event.listen(db.engine, 'connect', register_functions)

    app.register_blueprint(model_blueprint)
    app.register_blueprint(query_blueprint)
    app.register_blueprint(root_blueprint)

    model.init_context_processor(app)

    template_filter.init_app(app)

    return app
