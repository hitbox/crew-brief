import sqlalchemy as sa

from flask import Blueprint
from flask import render_template
from flask import request
from flask.views import View

from file_zipper.model import FileType
from file_zipper.model import Glob
from file_zipper.model import Path
from file_zipper.model import Regex
from file_zipper.query import match_with_pdf_statement
from file_zipper.query import paths_without_match
from file_zipper.query import zip_paths_statement
from file_zipper.web.extension import db
from file_zipper.web.pluggable import ListView
from file_zipper.web.pluggable import ObjectView
from file_zipper.web.url import model_url_rule

query_blueprint = Blueprint('query', __name__)

@query_blueprint.route('/path-matches')
def pathmatches():
    """
    List of the PathMatch objects that describe a path matched against a regex
    and the data deserialized from schema.
    """
    pathmatches = db.paginate(sa.select(PathMatch))
    context = {
        'pathmatches': pathmatches,
    }
    return render_template('path_matches.html', **context)

@query_blueprint.route('/unmatched')
def unmatched():
    """
    View of paths that failed to match regex.
    """
    unmatched_paths = db.session.query(
        Path
    ).outerjoin(
        PathMatch,
        Path.id == PathMatch.path_id,
    ).filter(
        PathMatch.path_id == None,
    ).order_by(
        Path.path,
    )
    context = {
        'paths': unmatched_paths,
        'subtitle': 'Unmatched Paths',
    }
    return render_template('path.html', **context)

@query_blueprint.route('/match-path-data')
def match_path_data():
    """
    Find PDF that needs to be inserted into the ZIP files.
    """
    # TODO
    # - Should be ready to try matching again, now with consistent dates and
    #   datetimes strings.
    zip_paths_stmt = zip_paths_statement()
    paths = db.paginate(zip_paths_stmt)
    context = {
        'stmt': zip_paths_stmt,
        'paths': paths,
    }

    return render_template('match_path_data.html', **context)

@query_blueprint.route('/unmatched-paths')
def unmatched_paths():
    """
    View paths that failed to match regex.
    """
    stmt = paths_without_match()
    objects = db.paginate(stmt)
    context = {
        'model_class': Path,
        'objects': objects,
        'endpoint': 'model.path.instance',
        'subtitle': 'Unmatched Paths',
        'description': 'Paths failed to match regex.',
    }

    if 'statement' in request.args:
        if request.args['statement'].lower()[:1] in '1y':
            context['statement'] = str(stmt)

    return render_template('list.html', **context)

@query_blueprint.route('/match-zip-with-pdf/')
def match_zip_with_pdf_list():
    """
    List zip file paths and link to match with a pdf.
    """
    stmt = (
        sa.select(Path)
        .join(FileType, FileType.id == Path.file_type_id)
        .filter(FileType.mime_type == 'application/x-zip-compressed')
    )
    zip_paths = db.paginate(stmt)
    context = {
        'zip_paths': zip_paths,
    }
    return render_template('match-zip-with-pdf-list.html', **context)

@query_blueprint.route('/match-zip-with-pdf/<int:zip_path_id>')
def match_zip_with_pdf(zip_path_id):
    """
    Show PDF paths that match on data scraped from the paths.
    """
    zip_path = db.session.get(Path, zip_path_id)
    stmt = match_with_pdf_statement(zip_path_id)
    objects = db.paginate(stmt)
    # TODO
    # - Show scraped path data too.
    context = {
        'objects': objects,
        'model_class': Path,
        'endpoint': '',
        'statement': str(stmt),
        'subtitle': f'PDF files that match. {zip_path.path}',
    }
    return render_template('list.html', **context)
