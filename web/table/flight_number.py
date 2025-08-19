from markupsafe import Markup
from markupsafe import escape

from web.table.column_args import created_at_args
from web.table.column_args import updated_at_args

only_list = [
    'flight_number',
    'created_at',
    'updated_at',
]

flight_number_table_args = {
    'only': only_list,
    'sort_key': lambda html_column: only_list.index(html_column.key),
    'field_args': {
        'flight_number': {
            'label': 'Flight Number',
            'attrs': {
                'class': 'data',
            },
        },
        'created_at': created_at_args,
        'updated_at': updated_at_args,
    },
}
