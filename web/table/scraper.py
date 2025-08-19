from crew_brief.formatter import regexes_formatter
from crew_brief.formatter import schema_formatter

scraper_table_args = {
    'field_args': {
        'name': {
            'label': 'Name',
        },
        'description': {
            'label': 'Description',
        },
        'regexes': {
            'label': 'Regexes',
            'formatter': regexes_formatter,
        },
        'schema_object': {
            'label': 'Schema',
            'formatter': schema_formatter,
        },
    },
}
