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

# Table list of OSWalk objects with a link to the files they produced.
os_walk_html_table = Table([
    Column('name', label='Name'),
    Column('normalized_top', **normalized_top_field_args),
    Column(key=None, label='Files', formatter=link_to_files),
])

# by-walker/<int:id>
leg_file_html_table = Table([
    Column('path', **path_field_args),
    Column('modified_at', **modified_at_args),
    Column('leg_identifier', **leg_identifier_args),
])

parsed_files_html_table = Table([
    Column('path', **path_field_args),
    Column(
        'leg_identifier',
        label = 'Leg Identifier',
        formatter = leg_identifier_formatter,
    ),
    Column(
        'modified_at',
        label = 'Modified At',
    ),
])

complete_zip_table = Table([
    Column('path', **path_field_args),
    Column('leg_identifier', **leg_identifier_args),
    Column(
        'complete_at',
        label = 'Complete At',
        formatter = mdy_formatter,
    ),
])

incomplete_zip_files_table = Table([
    Column('path', **path_field_args),
    Column('leg_identifier', **leg_identifier_args),
    Column(
        'missing_members',
        label = 'Missing',
        formatter = lambda leg_file, missing_members:
            unordered_list(missing_members)
    ),
    Column('complete_at', label='Complete At'),
])

stats_table = Table([
    Column(
        key = 'mime',
        label = 'MIME',
    ),
    Column(
        key = 'is_really_zip',
        label = 'ZIP?',
        formatter = lambda instance, value: yesno_formatter(value),
    ),
    Column(
        key = 'count',
        label = 'Count',
        formatter = lambda instance, value:
            Markup(f'<span class="data">{int_formatter(value)}</span>')
    ),
])
