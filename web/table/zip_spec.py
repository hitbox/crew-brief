from crew_brief.formatter import required_members_formatter

only_list = [
    'name',
    'required_members',
    'description',
    'created_at',
    'updated_at',
]

zip_spec_table_args = {
    'only': only_list,
    'sort_key': lambda html_column: only_list.index(html_column.key),
    'field_args': {
        'name': {
            'label': 'Name',
        },
        'description': {
            'label': 'Description',
        },
        'required_members': {
            'formatter': required_members_formatter,
        },
    },
}
