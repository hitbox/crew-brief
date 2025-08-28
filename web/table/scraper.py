from crew_brief.formatter import regexes_formatter
from crew_brief.formatter import schema_formatter
from htmlkit import unordered_list

scraper_table_args = {
    'only': [ 
        'name',
        'description',
        '_steps',
    ],
    'field_args': {
        'name': {
            'label': 'Name',
        },
        'description': {
            'label': 'Description',
        },
        # TODO
        # - The new steps attribute is not showing.
        '_steps': {
            'label': 'Steps',
            'formatter': lambda scraper, _steps: unordered_list(_steps),
        },
        # Old attributes before "steps"
        #'regexes': {
        #    'label': 'Regexes',
        #    'formatter': regexes_formatter,
        #},
        #'schema_object': {
        #    'label': 'Schema',
        #    'formatter': schema_formatter,
        #},
    },
}
