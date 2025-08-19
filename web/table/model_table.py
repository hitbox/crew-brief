from crew_brief.model import get_models
from htmlkit import model_html_table

from .airline import airline_table_args
from .airport import airport_table_args
from .column_args import column_args
from .flight_number import flight_number_table_args
from .leg_file import leg_file_table_args
from .leg_identifier import leg_identifier_table_args
from .mime_type import mime_type_table_args
from .os_walk import os_walk_table_args
from .regex import regex_table_args
from .required_member import required_member_table_args
from .scraper import scraper_table_args
from .zip_spec import zip_spec_table_args

model_table_args = {
    'Airline': airline_table_args,
    'Airport': airport_table_args,
    'FlightNumber': flight_number_table_args,
    'LegFile': leg_file_table_args,
    'LegIdentifier': leg_identifier_table_args,
    'MimeType': mime_type_table_args,
    'OSWalk': os_walk_table_args,
    'Regex': regex_table_args,
    'RequiredMember': required_member_table_args,
    'Scraper': scraper_table_args,
    'ZipSpec': zip_spec_table_args,
}

model_tables = {}
for name, model in get_models().items():
    kwargs = model_table_args.get(name, {})
    kwargs.setdefault('include_relationships', True)
    model_tables[model] = model_html_table(model, **kwargs)
