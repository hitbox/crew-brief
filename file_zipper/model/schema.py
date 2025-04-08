import importlib

from functools import cached_property

import sqlalchemy.orm

from .base import Base
from .mixin import NameMixin

sa = sqlalchemy

class Schema(Base, NameMixin):
    """
    Convert strings to types after the regex picks the path apart.
    """

    __tablename__ = 'schema'

    __column_args__ = {
        'name': {
            'doc': 'Friendly name for path schema.',
        },
    }

    __display_order__ = [
        'name',
        'import_name',
        'path_parser',
    ]

    import_name = sa.Column(
        sa.String,
        sa.CheckConstraint('length(import_name) > 0'),
        nullable = False,
        unique = True,
        doc = 'Import path string.',
    )

    def _import(self, import_name):
        module_name, class_name = import_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    @sa.orm.validates('import_name')
    def validate_import_name(self, key, value):
        self._import(value)
        return value

    @cached_property
    def schema_class(self):
        """
        Resolve the schema class from import_name.
        """
        return self._import(self.import_name)

    @cached_property
    def instance(self):
        """
        Instantiate schema class from `schema_class` attribute.
        """
        return self.schema_class()
