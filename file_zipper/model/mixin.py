from functools import cached_property

import sqlalchemy

from sqlalchemy.orm import declared_attr

sa = sqlalchemy

class NameMixin:

    @declared_attr
    def name(cls):
        """
        Name column string that is unique and not nullable or empty.
        """
        kwargs = cls._column_args('name')

        args = kwargs.get('args', [])
        if not args:
            args.append(sa.CheckConstraint('length(name) > 0'))

        kwargs.setdefault('type_', sa.String)
        kwargs.setdefault('nullable', False)
        kwargs.setdefault('unique', True)

        return sa.Column(*args, **kwargs)

    @property
    def display_string(self):
        """
        A property with a consistent name for use in interfaces.
        """
        return self.name
