from abc import ABC
from abc import abstractmethod
from enum import EnumMeta
from enum import IntEnum

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class DatabaseEnumMeta(EnumMeta):
    """
    Mix ABC and Enum metaclasses into one.
    """

    def __new__(metaclass, name, bases, namespace, **kwargs):
        cls = super().__new__(metaclass, name, bases, namespace, **kwargs)

        # Enforce required attributes.
        required_attributes = ['__model__']
        for attribute in required_attributes:
            if attribute not in namespace:
                raise TypeError(f'{name} must define {attribute}')

        # Enforce required methods
        required_methods = ['get_model', 'db_instance']
        for method in required_methods:
            if not callable(getattr(cls, method, None)):
                raise TypeError(f'{name} must implement method: {method}')

        # Update extra attributes for members.
        if hasattr(cls, '__member_args__'):
            # Validate __member_args__ is a dict
            member_args = cls.__member_args__

            # Validate all keys are strings.
            # Requiring string here, because IntEnum. Unsure what is a better way.
            if not all(isinstance(key, str) for key in member_args):
                raise TypeError(f'All {cls}.__member_args__ keys must be strings.')

            # Enforce __member_args__ matches the enum members.
            enum_member_names = {e.name for e in cls}
            if set(member_args.keys()) != enum_member_names:
                raise ValueError(
                    f'{cls}.__member_args__ keys must exactly match enum member names.'
                    f' Missing: {enum_member_names - member_args.keys()},'
                    f' Extra: {member_args.keys() - enum_member_names}'
                )
                if not isinstance(member_args, dict):
                    raise TypeError(f'{cls}.__member_args__ is not a dict.')

            # Validate all values are dicts, and they all have exactly the same keys.
            values = iter(member_args.values())
            first = set(next(values).keys())
            for k, subdict in member_args.items():
                if set(subdict.keys()) != first:
                    raise ValueError(
                        f'{cls}.__member_args__ values are all expected to be'
                        f' dicts and have exactly the same keys.')

            for member, kwargs in member_args.items():
                for key, value in kwargs.items():
                    setattr(getattr(cls, member), key, value)

        return cls


class DatabaseIntEnumBase(IntEnum):
    """
    Base class for IntEnum enums backed by a real database object.
    """

    @classmethod
    def get_model(cls):
        """
        Update class level attribute __model__ to mapper if it is a string and
        return it.
        """
        if isinstance(cls.__model__, str):
            # Resolve model class from Base registry.
            model_name = cls.__model__
            model_map = {
                mapper.class_.__name__: mapper.class_
                for mapper in Base.registry.mappers
            }
            try:
                cls.__model__ = model_map[model_name]
            except KeyError:
                raise LookupError(f'Model {model_name} not found.')
        return cls.__model__

    def db_object(self, session):
        """
        Get the database object for enum using .value as the primary key.
        """
        return session.get(self._get_model_class(), self.value)

    def db_instance(self, **kwargs):
        """
        Return a new instance of the model associated with this enum.
        """
