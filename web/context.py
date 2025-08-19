import datetime

from abc import ABC
from abc import abstractmethod

from markupsafe import Markup

from crew_brief.model import LegFile
from crew_brief.model import OriginDate
from crew_brief.query import select_complete_zip_since
from crew_brief.query import select_leg_identifiers_with_partial
from web.breadcrumbs import build_breadcrumbs
from web.endpoint import url_for_edit
from web.endpoint import url_for_new

class ContextBase(ABC):

    @abstractmethod
    def get_statement(self, model):
        pass

    def get_context(self, context):
        return context


class RecentZipComplete(ContextBase):
    """
    ZIP files marked complete some number of hours ago.
    """

    def __init__(self, hours_ago):
        self.hours_ago = hours_ago
        self._since_datetime = None

    @property
    def since_datetime(self):
        if self._since_datetime is None:
            dt = datetime.datetime.now() - datetime.timedelta(hours=self.hours_ago)
            self._since_datetime = dt.replace(minute=0, second=0, microsecond=0)
        return self._since_datetime

    def get_statement(self, model):
        return (
            select_complete_zip_since(self.since_datetime)
            .order_by(LegFile.complete_at)
        )

    def get_context(self, context):
        context['description'] = Markup(
            f'<p>ZIP files marked complete since {self.since_datetime:%d%b%y %H%M} local.</p>'
        )
        return context


class GroupByLegIdentifier(ContextBase):
    """
    Context for grouping files by leg identifier. That is, the files to append
    to ZIP files.
    """

    def get_statement(self, model):
        stmt = select_leg_identifiers_with_partial()
        # Add ordering by leg identifier origin date, descending.
        stmt = stmt.join(OriginDate).order_by(OriginDate.origin_date.desc())
        return stmt


class TableContext(ContextBase):
    """
    Methods for the generic model tables' contexts.
    """

    def __init__(self, model):
        self.model = model

    def get_statement(self, model):
        return sa.select(model)

    def get_context(self, context):
        context.setdefault('breadcrumbs', build_breadcrumbs())
        context.setdefault('model', self.model)
        context.setdefault('new_url', url_for_new(self.model))
        return context


class InstanceContext(ContextBase):
    """
    Methods for the generic instances' views contexts.
    """

    def __init__(self, model):
        self.model = model

    def get_statement(self, model):
        return sa.select(model)

    def get_context(self, context):
        context.setdefault('edit_url', url_for_edit(context['instance']))
        return context
