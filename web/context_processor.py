from flask import current_app
from flask import request
from flask import url_for

def get_navigation_list():
    """
    Dynamically create a list of links for the top bar.
    """
    navigation_list = []

    if request.endpoint != 'core.root':
        navigation_list.append(
            {'href': url_for('core.root'), 'text': 'Back to root'},
        )

    navigation_list.extend([
        {'href': url_for('admin.index'), 'text': 'Admin'},
    ])
    return navigation_list

def init_app(app):
    """
    Application-wide context variables.
    """

    @app.context_processor
    def inject():
        """
        Injection for templates.
        """
        context = current_app.config.get('INJECT', {})
        context.setdefault('js_config', current_app.config.get('JS_INJECT', {}))
        context.setdefault('current_app', current_app)

        context.update({
            'navigation_list': get_navigation_list(),
        })

        return context
