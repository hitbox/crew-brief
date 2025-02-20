from flask import Blueprint
from flask import Flask
from flask import current_app
from flask import render_template

# TODO
# - Just throwing the web app stuff in its own file.
# - This probably doesn't work.

preview_blueprint = Blueprint('preview', __name__)

@preview_blueprint.route('/')
@preview_blueprint.route('/<top>')
def preview_root(top=None):
    if not top:
        # top dirs from config
        listing = [path_data(path) for path in current_app.config['tops']]
    elif is_zip(top):
        with zipfile.ZipFile(top) as _zipfile:
            listing = [info_data(info) for info in _zipfile.infolist()]
    else:
        listing = [path_data(os.path.join(top, filename)) for filename in os.listdir(top)]

    context = dict(
        listing = listing,
        top = top,
    )
    return render_template('www_preview.html', **context)

@preview_blueprint.route('/process/<path>/<member>')
def preview_process(path, member):

    html_template = template_env.get_template('crew_brief_table.html')

    with zipfile.ZipFile(path) as zip_file:
        with zip_file.open(member) as member_file:
            member_json = member_file.read()
            member_data = json.loads(member_json)
            template_context = dict(
                zip_namelist = zip_file.namelist(),
                zip_path = path,
                member_name = member,
                member_data = member_data,
                show_data = False,
            )
            return html_template.render(crew_briefs=[template_context])

def www_preview():
    """
    Return Flask app to preview what this utility does.
    """
    app = Flask(__name__)

    cp = configparser.ConfigParser()
    cp.read(os.environ[ENVIRON_CONFIG_KEY])

    app.config['tops'] = [
        os.path.normpath(val) for key, val in cp['www_preview'].items()
        if is_top_key(key)]

    app.config['processes'] = processes_from_config(cp)

    app.register_blueprint(preview_blueprint)

    return app
