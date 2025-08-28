from markupsafe import Markup
from markupsafe import escape
from sqlalchemy.orm import RelationshipProperty

from crew_brief.util import model_attributes

from .definition_list import DefinitionKey
from .definition_list import DefinitionList

def unordered_list(iterable, ul_attrs=None, li_attrs=None):
    if ul_attrs is None:
        ul_attrs = {}

    if li_attrs is None:
        li_attrs = {}

    ul = render_tag('ul', attrs=ul_attrs)
    html_list = [ul]

    li = render_tag('li', attrs=li_attrs)
    for obj in iterable:
        html_list.append(li)
        html_list.append(Markup(obj))
        html_list.append('</li>')

    html_list.append('</ul>')

    return Markup(''.join(html_list))

def render_tag(tag, attrs=None, self_closing=False):
    attrs = attrs or {}
    attr_str = ' '.join(f'{key}="{escape(val)}"' for key, val in attrs.items() if val is not None)
    closing = ' /' if self_closing else '>'
    tag_str = f'<{tag}'
    if attr_str:
        tag_str += ' ' + attr_str
    tag_str += closing
    return tag_str
