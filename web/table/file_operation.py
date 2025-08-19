from markupsafe import Markup

from crew_brief.model import Airport
from crew_brief.model import get_models
from htmlkit import Column
from htmlkit import Table
from htmlkit import model_html_table
from htmlkit import unordered_list
from web.field_args import leg_identifier_args
from web.field_args import modified_at_args
from web.field_args import normalized_top_field_args
from web.field_args import path_field_args
from crew_brief.formatter import int_formatter
from crew_brief.formatter import leg_identifier_formatter
from crew_brief.formatter import link_to_files
from crew_brief.formatter import mdy_formatter
from crew_brief.formatter import yesno_formatter

from .model_table import model_table_args

file_operation_table = Table([
    Column(
        'operation_type',
        label = 'Type',
        formatter = lambda obj, value: value.name,
    ),
    Column(
        'status',
        label = 'Status',
        formatter = lambda obj, value: value.name,
    ),
    Column(
        'enabled_at',
        label = 'Enabled',
    ),
    Column(
        'leg_file',
    ),
    Column(
        'target_file',
    ),
])
