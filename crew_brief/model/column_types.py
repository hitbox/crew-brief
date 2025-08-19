from datetime import datetime
from datetime import timezone

from sqlalchemy import Column
from sqlalchemy import TypeDecorator

from .expression import server_utc_now

class UTCDateTime(TypeDecorator):
    """
    DateTime type that enforces timezone aware datetimes and ensures aware
    datetime objects come back from the database.
    """

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """
        Raise for naive datetime.
        """
        if value is not None:
            if not isinstance(value, datetime):
                raise TypeError(
                    f'Expected datetime.datetime, got {type(value)}')
            if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
                raise ValueError(
                    'Naive datetime is not allowed, datetime must be timezone-aware')
        return value

    def process_result_value(self, value, dialect):
        """
        Ensure resulting datetime is timezone aware.
        """
        # Some DBs return naive datetimes even if timezone=True
        if value is not None and value.tzinfo is None:
            # Assume UTC if no tzinfo
            return value.replace(tzinfo=timezone.utc)
        return value

    @classmethod
    def as_column(cls, **kwargs):
        """
        Return a timezone aware DateTime column. By default, sets the time to
        utc now, falls back to utc now server side, and is not nullable.
        """
        kwargs.setdefault('default', lambda: datetime.now(timezone.utc))
        kwargs.setdefault('server_default', server_utc_now())
        kwargs.setdefault('nullable', False)
        return Column(cls, **kwargs)
