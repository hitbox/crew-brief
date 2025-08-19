from markupsafe import Markup
from markupsafe import escape

from web.table.column_args import created_at_args
from web.table.column_args import iata_code_args
from web.table.column_args import icao_code_args
from web.table.column_args import updated_at_args

only_list = [
    'iata_code',
    'icao_code',
    'created_at',
    'updated_at',
]

airport_table_args = {
    'only': only_list,
    'sort_key': lambda html_column: only_list.index(html_column.key),
    'field_args': {
        'iata_code': iata_code_args,
        'icao_code': icao_code_args,
        'created_at': created_at_args,
        'updated_at': updated_at_args,
    },
}
