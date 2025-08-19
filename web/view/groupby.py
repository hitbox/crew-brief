import calendar
import copy
import datetime
import os

from itertools import groupby
from operator import attrgetter

import click
import sqlalchemy as sa

from flask import Blueprint
from flask import abort
from flask import render_template
from flask import request
from flask import url_for
from markupsafe import Markup

from crew_brief.calendar_data import expand_month
from crew_brief.calendar_data import weekdays
from crew_brief.formatter import AttributeNames
from crew_brief.model import FileOperation
from crew_brief.model import LegFile
from crew_brief.model import LegIdentifier
from crew_brief.model import OSWalk
from crew_brief.model import OriginDate
from crew_brief.model import RequiredMember
from crew_brief.model import get_model_by_table_name
from crew_brief.query import select_complete_leg_files
from crew_brief.query import select_complete_zip_count_for_year_by_month_day
from crew_brief.query import select_files_for_unparsed_count_by_mime_and_is_zipfile
from crew_brief.query import select_missing_members_groups
from crew_brief.query import select_parsed_files
from crew_brief.query import select_unparsed_count_by_mime_and_is_zipfile
from crew_brief.query import select_yearly_complete_zip_count_by_date
from crew_brief.query import select_zip_files
from crew_brief.query import select_zip_files_missing_members
from htmlkit import model_html_table
from htmlkit import unordered_list
from web.breadcrumbs import build_breadcrumbs
from web.context import GroupByLegIdentifier
from web.context import RecentZipComplete
from web.extension import db
from web.generic import AttributeView
from web.generic import TableView
from web.helper import MonthZIPCount
from web.query_arg import is_true_string
from web.query_arg import page_title_for_model
from web.query_arg import statement_for_model
from web.table import complete_zip_table
from web.table import incomplete_zip_files_table
from web.table import leg_file_html_table
from web.table import model_table_args
from web.table import model_tables
from web.table import os_walk_html_table
from web.table import parsed_files_html_table

groupby_bp = Blueprint('groupby', __name__, url_prefix='/by')

@groupby_bp.context_processor
def context_processor():
    return {'breadcrumbs': build_breadcrumbs()}

@groupby_bp.route('/<table>/<path:attrnames>')
def attr(table, attrnames):
    """
    View a table grouped by given attribute names.
    """
    model = get_model_by_table_name(table)
    if not model:
        abort(400, description=f'Model not found for table name {table}')

    attrnames = attrnames.split('/')

    stmt = sa.select(model)
    for name in attrnames:
        attr = getattr(model, name)
        stmt = stmt.where(attr != None)

    pagination = db.paginate(stmt)

    # TODO
    # - Sorting for all attribute names.
    # - Reverse sorting.
    key = attrgetter(*attrnames)

    grouped = sorted(pagination.items, key=key)
    grouped = groupby(grouped, key=key)
    grouped = [(key, list(grouper)) for key, grouper in grouped]

    context = {
        'grouped': grouped,
        'pagination': pagination,
        'attrnames': AttributeNames(attrnames),
        'table': model_tables[model],
        'model': model,
    }

    return render_template('table_grouped.html', **context)

@groupby_bp.route('/missing-member-groups')
def missing_members_groups():
    """
    Cards of unique groups of missing members and a link to the files.
    """
    grouped_stmt = select_missing_members_groups()
    rows = []
    for required_member_ids, leg_file_ids, set_size in db.session.execute(grouped_stmt):
        required_members = db.session.scalars(
            db.select(RequiredMember)
            .where(RequiredMember.id.in_(required_member_ids))
        )
        rows.append({
            'required_member_ids': required_member_ids,
            'required_members': required_members,
            'set_size': set_size,
            'n_files': len(leg_file_ids),
        })

    rows = sorted(rows, key=lambda d: d['n_files'], reverse=True)
    context = {
        'rows': rows,
    }
    return render_template('missing_members_groups.html', **context)

@groupby_bp.route('/missing-member-groups/files/<list:required_member_ids>')
def files_by_missing_members_group(required_member_ids):
    """
    Paginated view of files missing a particular set of required members.
    """
    required_member_ids = sorted(set(map(int, required_member_ids)))
    leg_file_ids_stmt = select_zip_files_missing_members(required_member_ids)
    leg_files_stmt = (
        db.select(LegFile)
        .where(
            LegFile.id.in_(db.session.scalars(leg_file_ids_stmt))
        )
        .order_by(LegFile.mtime.desc())
    )
    pagination = db.paginate(leg_files_stmt)

    required_members = db.session.scalars(
        db.select(RequiredMember)
        .where(RequiredMember.id.in_(required_member_ids))
    )
    required_member_names = [rm.filename for rm in required_members]

    page_title = [
        Markup(f'<h3>ZIP Files Missing {len(required_member_names):,} members:</h3>'),
        unordered_list(Markup(f'<span class="data">{name}</span>') for name in required_member_names),
        Markup(f'<p><a href="{ url_for('.missing_members_groups') }">Back to missing members groups</a>'),
    ]

    if pagination.total > 1:
        # Update the formatter
        commonpath = os.path.commonpath(leg_file.path for leg_file in pagination)
        page_title.append(Markup(f'<p>Paths relative to <span class="data">{commonpath}</span></p>'))
        page_title.append(Markup(f'<p>Click to copy full path to clipboard.</p>'))

    context = {
        'model_class': LegFile,
        'page_title': Markup(''.join(map(Markup, page_title))),
        'pagination': pagination,
        'table': model_tables[LegFile],
    }
    return render_template('table.html', **context)

@groupby_bp.route('/unparsed')
def unparsed():
    """
    Unparsed files by their mime type and detected type.
    """
    stmt = select_unparsed_count_by_mime_and_is_zipfile()
    unparsed_by_file_type = db.session.execute(stmt).mappings().all()
    context = {
        'unparsed_by_file_type': unparsed_by_file_type,
    }
    return render_template('unparsed_by_file_type.html', **context)

@groupby_bp.route('/unparsed/<bool:is_zipfile>/<path:mime>')
def unparsed_list(is_zipfile, mime):
    """
    Table listing of unparsed files for is_zipfile and mime type.
    """
    stmt = select_files_for_unparsed_count_by_mime_and_is_zipfile(is_zipfile, mime)
    pagination = db.paginate(stmt)
    context = {
        'table': model_tables[LegFile],
        'pagination': pagination,
    }
    return render_template('table.html', **context)

@groupby_bp.route('/complete-zip/year/<int:year>')
def complete_by_year(year):
    """
    ZIP files marked complete statistics for a year, in groups of months and days.
    """
    stmt = select_yearly_complete_zip_count_by_date(year)
    for_date = dict(db.session.execute(stmt).all())

    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    year_data = [
        expand_month(month_number, year=year, cal=cal, today=datetime.date.today())
        for month_number in range(1, 13)
    ]
    context = {
        'for_date': for_date,
        'weekdays': weekdays(cal),
        'year_data': year_data,
        'year': year,
    }
    return render_template('complete_by_year.html', **context)

@groupby_bp.route('/complete-zip/year/<int:year>/<int:month>')
def complete_by_year_month(year, month):
    """
    ZIP files marked complete statistics for a year, in groups of months and days.
    """
    stmt = select_yearly_complete_zip_count_by_date(year)
    for_date = dict(db.session.execute(stmt).all())

    today = datetime.date.today()

    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month_zip_count = MonthZIPCount(year, month, today, cal)

    year_data = [
        expand_month(month_number, year=year, cal=cal, today=datetime.date.today())
        for month_number in range(1, 13)
    ]
    context = {
        'for_date': for_date,
        'weekdays': weekdays(cal),
        'year_data': year_data,
        'year': year,
        'month_zip_count': month_zip_count,
    }
    return render_template('complete_by_year_month.html', **context)

groupby_bp.add_url_rule(
    '/files',
    view_func = TableView.as_view(
        'files',
        model_class = LegFile,
        table = model_tables[LegFile],
        template = 'table.html',
        get_statement = sa.select(LegFile),
        get_context = lambda context: context,
    ),
)

groupby_bp.add_url_rule(
    '/parsed-files',
    view_func = TableView.as_view(
        'parsed_files',
        model_class = LegFile,
        table = parsed_files_html_table,
        template = 'table.html',
        get_statement = lambda model:
            select_parsed_files(
                LegFile,
                is_zipfile = is_true_string(request.args.get('is_zipfile', ''))
            ),
        get_context = lambda context: context,
    ),
)

groupby_bp.add_url_rule(
    '/is-zipfile',
    view_func = TableView.as_view(
        'is_zipfile',
        model_class = LegFile,
        table = incomplete_zip_files_table,
        template = 'table.html',
        get_statement = lambda model:
            select_zip_files().order_by(LegFile.mtime),
        get_context = lambda context: context,
    ),
)

groupby_bp.add_url_rule(
    '/is-complete-zip',
    view_func = TableView.as_view(
        'is_complete_zip',
        model_class = LegFile,
        table = complete_zip_table,
        template = 'table.html',
        get_statement = lambda model: select_complete_leg_files().order_by(LegFile.mtime),
        get_context = lambda context: context,
    ),
)

# Table listing complete ZIP files for date.
groupby_bp.add_url_rule(
    '/is-complete-zip/<date:date>',
    view_func = TableView.as_view(
        'is_complete_zip_for_date',
        model_class = LegFile,
        table = complete_zip_table,
        template = 'table.html',
        get_statement = lambda model:
            select_complete_leg_files()
            .where(LegFile.complete_at_date == request.view_args['date'])
            .order_by(LegFile.mtime),
        get_context = lambda context: context,
    ),
)

groupby_bp.add_url_rule(
    '/walker',
    view_func = TableView.as_view(
        'list',
        model_class = OSWalk,
        table = os_walk_html_table,
        template = 'table.html',
        get_statement = statement_for_model,
        get_context = lambda context: context,
    ),
)

groupby_bp.add_url_rule(
    '/walker/<int:id>',
    view_func = AttributeView.as_view(
        'walker_files',
        model_class = OSWalk,
        table = leg_file_html_table,
        attribute = 'leg_files',
        template = 'table.html',
        page_title = Markup('<h2>Files by names OS file walker.</h2>'),
        get_statement = statement_for_model,
        get_context = lambda context: context,
    ),
)

recent_zip_complete = RecentZipComplete(hours_ago=2)

groupby_bp.add_url_rule(
    '/recent-zip-complete',
    view_func = TableView.as_view(
        'recent_zip_complete',
        model_class = LegFile,
        table = complete_zip_table,
        template = 'table.html',
        get_statement = recent_zip_complete.get_statement,
        get_context = recent_zip_complete.get_context,
    ),
)

# Files grouped by leg identifiers. That is, the files that should be added to
# ZIP files.

group_by_leg_identifier = GroupByLegIdentifier()

groupby_bp.add_url_rule(
    '/leg-identifer',
    view_func = TableView.as_view(
        'leg_identifier',
        model_class = LegIdentifier,
        table = model_tables[LegIdentifier],
        template = 'grouped_leg_identifier.html',
        get_statement = group_by_leg_identifier.get_statement,
        get_context = group_by_leg_identifier.get_context,
    ),
)

from web.table.file_operation import file_operation_table

groupby_bp.add_url_rule(
    '/file-operation',
    view_func = TableView.as_view(
        'file_operation',
        model_class = FileOperation,
        table = file_operation_table,
        template = 'table.html',
        get_statement = lambda model: sa.select(model),
        get_context = lambda context: context,
    ),
)

# Sub-commands

@groupby_bp.cli.command('show-unparsed-paths')
@click.argument('is_zipfile', type=bool)
@click.argument('mime', type=str)
def show_unparsed_paths(is_zipfile, mime):
    """
    Print unparsed files for arguments line by line.
    """
    stmt = select_files_for_unparsed_count_by_mime_and_is_zipfile(is_zipfile, mime)
    for leg_file in db.session.scalars(stmt):
        try:
            click.echo(leg_file.path)
        except UnicodeEncodeError:
            click.echo(f'Unable to print leg_file.path for id: {leg_file.id}')
