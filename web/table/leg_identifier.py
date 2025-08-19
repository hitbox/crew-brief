from markupsafe import Markup

from htmlkit import unordered_list
from web.endpoint import url_for_instance
from web.field_args import scraped_by_args
from crew_brief.formatter import AttributeLink
from crew_brief.formatter import leg_file_formatter
from crew_brief.formatter import path_formatter

only_list = [
    'airline',
    'flight_number_object',
    'origin_date_object',
    'departure_airport',
    'destination_airport',
    'ofp_version',
    'datetime',
    'leg_file', # misnamed, actually a list
    'scraped_by',
]

leg_identifier_table_args = {
    'only': only_list,
    'sort_key': lambda html_column: only_list.index(html_column.key),
    'field_args': {
        'departure_airport': {
            'formatter': AttributeLink('iata_code', {'class': 'data'}),
        },
        'destination_airport': {
            'formatter': AttributeLink('iata_code', {'class': 'data'}),
        },
        'scraped_by': scraped_by_args,
        'leg_file': {
            'formatter': lambda instance, leg_files: leg_file_formatter(leg_files),
        },
    },
}
