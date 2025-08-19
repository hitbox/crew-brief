from markupsafe import Markup
from markupsafe import escape

from crew_brief.formatter import none_markup
from crew_brief.util import abbreviate
from web.endpoint import url_for_instance

only_list = [
    'scraper',
    'name',
    'position',
    'pattern',
    'description',
]

regex_table_args = {
    'only': only_list,
    'sort_key': lambda html_column: only_list.index(html_column.key),
    'field_args': {
        'name': {
            'label': 'Name',
        },
        'description': {
            'label': 'Description',
        },
        'pattern': {
            'label': 'Pattern',
            'formatter': lambda instance, value:
                Markup(f'<code>{escape(abbreviate(value))}</code>')
        },
        'scraper': {
            'label': 'Scraper Object',
            'formatter': lambda regex, attr:
                Markup(f'<a href="{url_for_instance(regex.scraper)}">{regex.scraper.name}</a>')
                if regex.scraper else
                none_markup
            ,
        },
    },
}
