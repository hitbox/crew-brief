from web.field_args import leg_identifier_args
from web.field_args import modified_at_args
from web.field_args import path_field_args
from crew_brief.formatter import mdy_formatter
from crew_brief.formatter import missing_members_formatter
from crew_brief.formatter import yesno_formatter

only_list = [
    'path',
    'leg_identifier',
    'parse_exception_at',
    'is_zipfile',
    'mime_type',
    'check_complete_at',
    'modified_at',
]

leg_file_table_args = {
    'only': only_list,
    'sort_key': lambda html_column: only_list.index(html_column.key),
    'field_args': {
        'mime_type': {
            'label': 'MIME',
        },
        'path': path_field_args,
        'is_zipfile': {
            'label': 'ZIP?',
            'formatter': lambda inst, val: yesno_formatter(val),
        },
        'missing_members': {
            'formatter': missing_members_formatter,
        },
        'leg_identifier': leg_identifier_args,
        'check_complete_at': {
            'label': 'Completeness Check At',
            'formatter': mdy_formatter,
        },
        'modified_at': modified_at_args,
        'parse_exception_at': {
            'label': 'Parse Exception At',
            'formatter': mdy_formatter,
        },
    },
}
