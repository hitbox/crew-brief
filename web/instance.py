from markupsafe import Markup

from htmlkit import unordered_list
from web.endpoint import url_for_instance
from web.field_args import created_at_args
from web.field_args import leg_file_args
from web.field_args import leg_identifier_args
from web.field_args import matching_files_args
from web.field_args import modified_at_args
from web.field_args import normalized_top_field_args
from web.field_args import path_field_args
from web.field_args import scraped_by_args
from crew_brief.formatter import airport_formatter

leg_identifer_only = [
    'airline',
    'flight_number_object',
    'origin_date_object',
    'departure_airport',
    'destination_airport',
    'ofp_version',
    'ofp_version_object',
    'datetime',
    'leg_file', # misnamed, actually a list
    'matching_files',
    'scraped_by',
]

model_instance_args = {
    'LegIdentifier': {
        'only': leg_identifer_only,
        'sort_key': lambda html_column: leg_identifer_only.index(html_column.key),
        'field_args': {
            'departure_airport': {
                'formatter': lambda instance, value: airport_formatter(value),
            },
            'destination_airport': {
                'formatter': lambda instance, value: airport_formatter(value),
            },
            'scraped_by': scraped_by_args,
            'leg_file': leg_file_args,
            'matching_files': matching_files_args,
        },
    },
}
