from datetime import datetime
from enum import IntEnum

import sqlalchemy as sa

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import object_session
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from crew_brief.model.base import Base
from crew_brief.model.base import DatabaseEnumMeta
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin

class ChangeStatusEnum(IntEnum, metaclass=DatabaseEnumMeta):
    """
    Type of change in the history of a record.
    """

    __model__ = 'ChangeStatus'

    CREATED = 1
    UPDATED = 2
    DELETED = 3

    @classmethod
    def get_model(cls):
        return ChangeStatus

    def db_instance(self):
        model = self.get_model()
        return model(
            id = self.value,
            name = self.name,
        )


class ChangeStatus(Base):
    """
    The type of change in a history shadow table.
    """

    __tablename__ = 'change_status'

    id = Column(
        Integer,
        primary_key = True,
    )

    name = Column(
        String,
        unique = True,
    )


class HistoryMixin:

    @declared_attr
    def change_status_id(cls):
        return Column(
            ForeignKey('change_status.id'),
            nullable = False,
        )

    @declared_attr
    def change_status(cls):
        return relationship(
            'ChangeStatus',
            foreign_keys = [cls.change_status_id],
        )

    @declared_attr
    def changed_at(cls):
        return Column(
            DateTime,
            nullable = False,
            server_default = sa.func.now(),
            doc = 'Datetime of this change.',
        )

    @declared_attr
    def changed_by_id(cls):
        return Column(
            ForeignKey('user.id'),
            nullable = False,
        )

    @declared_attr
    def changed_by(cls):
        return relationship(
            'User',
        )
