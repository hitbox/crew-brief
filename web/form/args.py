from wtforms.widgets import TextArea

model_form_args = {
    'Regex': {
        'only': [
            'name',
            'scraper',
            'description',
            'pattern',
            'position',
        ],
        'field_args': {
            'scraper': {
                'get_label': 'name',
            },
            'pattern': {
                'widget': TextArea(),
                'render_kw': {
                    'rows': 10,
                    'cols': 80,
                },
            },
            'description': {
                'widget': TextArea(),
                'render_kw': {
                    'rows': 10,
                    'cols': 80,
                },
            },
        }
    },
    'LegFile': {
        'exclude': [
            'leg_identifier',
            'missing_members',
            'mtime',
        ],
    },
    'Scraper': {
        'field_args': {
            'regexes': {
                'get_label': 'name',
            },
            'schema_object': {
                'get_label': 'name',
            },
        },
    },
    'LegIdentifier': {
        'only': [
            'airline',
            'flight_number_object',
            'origin_date_object',
            'departure_airport',
            'destination_airport',
            'ofp_version',
            'datetime',
        ],
    },
}
