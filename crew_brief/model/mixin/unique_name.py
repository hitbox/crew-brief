from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import declared_attr

class UniqueNameMixin:
    """
    Mixin a unique name column.
    """

    @declared_attr
    def name(cls):
        return Column(
            String,
            nullable = True,
            unique = True,
        )
