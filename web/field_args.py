import json
import os

from flask import url_for
from markupsafe import Markup
from markupsafe import escape

from crew_brief.model import get_models
from htmlkit import model_html_table
from htmlkit import unordered_list
from htmlkit.table import Column
from htmlkit.table import Table
from web.endpoint import url_for_instance
from crew_brief.formatter import AttributeLink
from crew_brief.formatter import leg_identifier_formatter
from crew_brief.formatter import link_to_files
from crew_brief.formatter import many_path_formatter
from crew_brief.formatter import mdy_formatter
from crew_brief.formatter import missing_members_formatter
from crew_brief.formatter import none_markup
from crew_brief.formatter import path_formatter
from crew_brief.formatter import regexes_formatter
from crew_brief.formatter import required_members_formatter
from crew_brief.formatter import schema_formatter
from crew_brief.formatter import yesno_formatter

path_field_args = {
    'label': 'Path',
    'formatter': lambda instance, value: path_formatter(value),
}

leg_identifier_args = {
    'label': 'Leg Identifier',
    'formatter': leg_identifier_formatter,
}

scraped_by_args = {
    'label': 'Scraped By',
    'formatter': AttributeLink('name', {'class': 'data'}),
}

created_at_args = {
    'label': 'Created At',
    'formatter': mdy_formatter,
}

modified_at_args = {
    'label': 'Modified At',
    'formatter': mdy_formatter,
}

normalized_top_field_args = {
    'label': 'Top',
    'formatter': lambda instance, value: path_formatter(value),
}

matching_files_args = {
    'formatter': lambda instance, value: many_path_formatter(value),
}

leg_file_args = {
    'formatter': lambda instance, leg_files:
        unordered_list(
            Markup(f'<a href="{url_for_instance(leg_file)}">{path_formatter(leg_file.path)}</a>')
            for leg_file in leg_files
        ),
}
