from markupsafe import Markup
from markupsafe import escape

from crew_brief.util import abbreviate
from htmlkit import unordered_list
from web.endpoint import url_for_instance
from web.field_args import leg_identifier_args
from web.field_args import modified_at_args
from web.field_args import path_field_args
from web.field_args import scraped_by_args
from crew_brief.formatter import yesno_formatter

mime_type_table_args = {
    'field_args': {
        'mime': {
            'label': 'MIME',
        },
        'is_mime_zip': {
            'label': 'ZIP?',
            'formatter': lambda inst, val: yesno_formatter(val),
        },
    },
}
