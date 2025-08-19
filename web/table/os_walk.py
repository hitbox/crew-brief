from crew_brief.formatter import yesno_formatter
from web.table.column_args import created_at_args
from web.table.column_args import iata_code_args
from web.table.column_args import icao_code_args
from web.table.column_args import updated_at_args

only_list = [
    'name',
    #'top',
    'normalized_top',
    'topdown',
    'followlinks',
    'path_flavor',
    'created_at',
    'updated_at',
]

def sort_key(html_column):
    return only_list.index(html_column.key)

os_walk_table_args = {
    'only': only_list,
    'sort_key': sort_key,
    'field_args': {
        'created_at': created_at_args,
        'updated_at': updated_at_args,
        'name': {
            'label': 'Name',
        },
        'normalized_top': {
            'label': 'Top',
        },
        'topdown': {
            'label': 'Top Down?',
            'formatter': lambda instance, value: yesno_formatter(value),
        },
        'followlinks': {
            'label': 'Follow Links?',
            'formatter': lambda instance, value: yesno_formatter(value),
        },
        'path_flavor': {
            'label': 'Flavor',
            'formatter': lambda instance, value: value.name,
        },
    },
}
