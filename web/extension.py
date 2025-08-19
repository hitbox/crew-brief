from flask_sqlalchemy import SQLAlchemy

from crew_brief.model import Base

db = SQLAlchemy(model_class=Base)

def init_app(app):
    db.init_app(app)
