from .core import core_bp
from .find import find_bp
from .groupby import groupby_bp
from .model import model_bp

def init_app(app):
    app.register_blueprint(core_bp)
    app.register_blueprint(find_bp)
    app.register_blueprint(groupby_bp)
    app.register_blueprint(model_bp)
