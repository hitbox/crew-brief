from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import validates

class NonEmptyStringMixin:
    """
    Prevent empty strings mixin.
    """

    @staticmethod
    def _is_string(column):
        return (
            isinstance(column, Column)
            and isinstance(column.type, String)
            # Not an Enum
            and not isinstance(column.type, Enum)
        )

    @declared_attr
    def __table_args__(cls):
        constraints = []
        for name, column in cls.__dict__.items():
            if cls._is_string(column):
                constraints.append(CheckConstraint(f"{name} <> ''"))
        return tuple(constraints)

    @classmethod
    def __declare_last__(cls):
        for name, column in cls.__dict__.items():
            if cls._is_string(column):
                cls._add_non_empty_validator(name)

    @classmethod
    def _add_non_empty_validator(cls, attr):
        def validate(self, key, value):
            if not value or not value.strip():
                raise ValueError(f'{key} must not be empty')
            return value
        setattr(cls, f'validate_{attr}', validates(attr)(validate))
