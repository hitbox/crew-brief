from flask import Blueprint
from flask import render_template
from flask.views import View

from file_zipper.model import Glob
from file_zipper.model import Path
from file_zipper.model import Regex
from file_zipper.web.extension import db
from file_zipper.web.pluggable import ListView
from file_zipper.web.pluggable import ObjectView
from file_zipper.web.url import model_url_rule

root_blueprint = Blueprint('root', __name__)

@root_blueprint.route('/')
def index():
    return render_template('index.html')
