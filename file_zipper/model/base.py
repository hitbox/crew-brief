import datetime

import sqlalchemy.orm

from sqlalchemy.orm import declared_attr

sa = sqlalchemy

class Base(sa.orm.DeclarativeBase):

    @declared_attr
    def created_at(cls):
        return sa.Column(
            sa.DateTime,
            default = datetime.datetime.utcnow,
            nullable = False,
        )

    @declared_attr
    def updated_at(cls):
        return sa.Column(
            sa.DateTime,
            default = datetime.datetime.utcnow,
            onupdate = datetime.datetime.utcnow,
            nullable = False,
        )

    @declared_attr
    def id(cls):
        kwargs = cls._column_args('id')
        kwargs.setdefault('type_', sa.Integer)
        kwargs.setdefault('primary_key', True)
        return sa.Column(**kwargs)


    @classmethod
    def _column_args(cls, colname):
        return getattr(cls, '__column_args__', {}).get(colname, {})
