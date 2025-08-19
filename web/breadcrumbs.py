from flask import request
from flask import url_for

def build_breadcrumbs(*more):
    """
    Create list of tuples (href, text) for use as breadcrumb links.
    """
    breadcrumbs = []
    if request.endpoint != 'core.root':
        breadcrumbs.append((url_for('core.root'), 'Back to root'))
    for href, text in more:
        breadcrumbs.append((href, text))
    return breadcrumbs
