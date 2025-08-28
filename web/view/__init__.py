from .admin import admin_bp
from .core import core_bp
from .find import find_bp
from .groupby import groupby_bp

def init_app(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(core_bp)
    app.register_blueprint(find_bp)
    app.register_blueprint(groupby_bp)
