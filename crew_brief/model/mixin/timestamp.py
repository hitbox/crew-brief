from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import declared_attr

from crew_brief.formatter import mdy_formatter

class TimestampMixin:
    """
    Record created and update time stamps.
    """

    @declared_attr
    def created_at(cls):
        return Column(
            DateTime,
            nullable = False,
            server_default = func.now(),
            info = {
                'label': 'Created At',
                'formatter': mdy_formatter,
            },
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            nullable = False,
            server_default = func.now(),
            onupdate = func.now(),
            info = {
                'label': 'Updated At',
                'formatter': mdy_formatter,
            },
        )
