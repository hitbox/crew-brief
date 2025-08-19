import datetime
import json
import os

from flask import url_for
from markupsafe import Markup
from markupsafe import escape

from crew_brief.util import abbreviate
from crew_brief.util import split_at
from htmlkit import render_tag
from htmlkit import unordered_list

from web.endpoint import url_for_instance

none_markup = Markup('(None)')

class AttributeNames:

    def __init__(self, attrnames):
        self.attrnames = attrnames

    def __html__(self):
        html = []
        for name in self.attrnames:
            html.append(f'<span>{Markup(name)}</span>')
        return Markup(', '.join(html))


class AttributeLink:

    def __init__(self, key, attrs=None):
        self.key = key
        self.attrs = attrs

    def __call__(self, instance, value):
        if value is None:
            return none_markup

        if self.attrs:
            attrs = self.attrs.copy()
        else:
            attrs = {}
        url = url_for_instance(value)
        attrs.setdefault('href', url)
        open_tag = render_tag('a', attrs)
        text = getattr(value, self.key)
        return Markup(f'{open_tag}{text}</a>')


def missing_members_formatter(leg_file, missing_members):
    if missing_members:
        return unordered_list(missing_members)
    else:
        return none_markup

def regexes_formatter(scraper, regexes):
    items = (f'<a href="{url_for_instance(regex)}">{regex.name}</a>' for regex in regexes)
    return unordered_list(items)

def schema_formatter(scraper, schema):
    if scraper is None or schema is None:
        return none_markup
    return Markup(f'<a href="{url_for_instance(schema)}">{schema.name}</a>')

def required_members_formatter(inst, required_members):
    items = (f'<a href="{url_for_instance(rm)}">{rm.filename}</a>' for rm in required_members)
    return unordered_list(items, li_attrs = {'class': 'data'})

def leg_identifier_formatter(inst, leg_identifier):
    if leg_identifier is None:
        return none_markup
    url = url_for_instance(leg_identifier)
    parts = leg_identifier.as_parts()
    text = unordered_list(parts, ul_attrs={'class': 'token-list'})
    return Markup(f'<a class="data" href="{url}">{text}</a>')

def link_to_files(inst, value):
    url = url_for('groupby.walker_files', id=inst.id)
    return Markup(f'<a href="{url}">List files...</a>')

def mdy(dt):
    if dt is None:
        return none_markup
    else:
        return Markup(f'<span class="oneline">{dt.strftime('%d%b%y %H:%M')}</span>')

def mdy_formatter(instance, dt):
    return mdy(dt)

def data_formatter(value):
    return Markup(f'<span class="data">{ value }</span>')

def path_formatter(path):
    return Markup(f'<span class="data filepath">{ Markup(path) }</span>')

def many_path_formatter(paths):
    return unordered_list(path_formatter(path) for path in paths)

def yesno_formatter(value):
    if value is True:
        text = 'Yes'
    else:
        text = 'No'
    return Markup(text)

def airport_formatter(value):
    return Markup(f'<a href="{url_for_instance(value)}">{value.iata_code}</a>')

def int_formatter(value):
    return Markup(f'<span>{value:,}</span>')

def leg_file_formatter(leg_files):
    html_list = []
    for leg_file in leg_files:

        path = leg_file.path
        if len(path) > 40:
            before, after = split_at(path, 40)
            path = Markup(
                f'<span class="data filepath">'
                f'<span class="abbreviated">{before}</span>'
                f'<span>{after}</span>'
                f'</span>')

        text = path_formatter(path)
        url = url_for_instance(leg_file)
        html_list.append(Markup(f'<a href="{url}">{text}</a>') )

    return unordered_list(html_list)
