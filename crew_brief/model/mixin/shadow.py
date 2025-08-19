from datetime import datetime
from datetime import timezone

import sqlalchemy as sa

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import event
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import relationship

from crew_brief.model.base import Base
from crew_brief.model.change_type import ChangeType
from crew_brief.model.change_type_enum import ChangeTypeEnum

from .audit_helper import AuditHelper

class ShadowHistoryMixin:
    """
    Mixin that automatically creates shadow history table and functionality.
    """

    __shadow_history_args__ = {
        'class_suffix': 'History',
        'table_suffix': '_history',
    }

    @classmethod
    def audit(cls):
        """
        Instantiate a helper object for this class and it's shadow history,
        with useful functions for auditing the history of records. This method
        is mainly a namespace. Would prefer a class property.
        """
        return AuditHelper(cls)

    @declared_attr
    def history(cls):
        """
        Relationship to history records
        """
        history_args = cls.__shadow_history_args__
        history_class_name = f'{cls.__name__}{history_args["class_suffix"]}'
        return relationship(
            history_class_name,
            back_populates = cls.__tablename__,
            cascade = 'all, delete-orphan',
            order_by = f'{history_class_name}.change_timestamp.desc()'
        )

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Automatically create history table when class is defined
        """
        super().__init_subclass__(**kwargs)
        cls._create_history_table()
        cls._setup_event_listeners()

    @classmethod
    def _create_history_table(cls):
        """
        Dynamically create the shadow history table
        """
        history_args = cls.__shadow_history_args__
        history_class_name = f'{cls.__name__}{history_args["class_suffix"]}'
        history_table_name = f'{cls.__tablename__}{history_args["table_suffix"]}'

        # Build columns dictionary
        history_columns = {
            'id': Column(Integer, primary_key=True),
            'change_type_id': Column(
                Integer,
                ForeignKey('change_type.id'),
                nullable = False,
            ),
            'change_timestamp': Column(
                DateTime(timezone=True),
                default = lambda: datetime.now(timezone.utc),
                nullable = False,
            ),
            # XXX
            'operation_user': Column(String(50)),
        }

        for column in cls.__table__.columns:
            if column.primary_key:
                # Create FK back to original PK.
                new_name = f'{cls.__tablename__}_{column.name}'
                new_column = Column(
                    column.type,
                    ForeignKey(
                        column,
                        ondelete = 'SET NULL'
                    ),
                    primary_key = False,
                    autoincrement = False,
                    nullable = True,
                )
                history_columns[new_name] = new_column
            else:
                # Copy regular columns
                new_column = Column(
                    column.type,
                    *column.constraints,
                    nullable = column.nullable,
                )
                history_columns[column.name] = new_column

        # Add relationships
        history_columns['change_type'] = relationship(
            'ChangeType',
        )
        # Relationship back to original model.
        history_columns[cls.__tablename__] = relationship(
            cls.__name__,
            back_populates = 'history',
            foreign_keys = [
                history_columns[
                    f'{cls.__tablename__}_{cls.__table__.primary_key.columns.keys()[0]}'
                ]
            ],
        )

        # Create the history class
        bases = (
            Base,
        )
        attributes = {
            '__tablename__': history_table_name,
            **history_columns,
        }
        history_class = type(history_class_name, bases, attributes)

        # Store reference for event listeners
        cls._history_class = history_class

        return history_class

    @classmethod
    def _setup_event_listeners(cls):
        """
        Setup automatic history tracking events
        """

        @event.listens_for(cls, 'after_insert')
        def create_insert_history(mapper, connection, target):
            cls._create_history_record(connection, target, ChangeTypeEnum.INSERT)

        @event.listens_for(cls, 'after_update')
        def create_update_history(mapper, connection, target):
            cls._create_history_record(connection, target, ChangeTypeEnum.UPDATE)

        @event.listens_for(cls, 'after_delete')
        def create_delete_history(mapper, connection, target):
            cls._create_history_record(connection, target, ChangeTypeEnum.DELETE)

    @classmethod
    def _create_history_record(cls, connection, target, change_type):
        """
        Create a history record
        """
        # Get the primary key value
        pk_column = list(cls.__table__.primary_key.columns)[0]
        pk_value = getattr(target, pk_column.name)

        # Build the history record data
        history_data = {
            f'{cls.__tablename__}_{pk_column.name}': pk_value,
            'change_type_id': change_type.value,
            'change_timestamp': datetime.now(timezone.utc),
        }

        # Copy all non-PK column values
        for column in cls.__table__.columns:
            if not column.primary_key:
                history_data[column.name] = getattr(target, column.name)

        # Insert the history record
        connection.execute(
            cls._history_class.__table__.insert().values(**history_data)
        )
