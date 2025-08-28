from inspect import isclass

import sqlalchemy as sa

from sqlalchemy.orm import aliased
from sqlalchemy.orm import foreign
from sqlalchemy.orm import relationship
from sqlalchemy.orm import remote

from . import archive
from . import rowifier
from . import source
from . import user_event
from . import workbook
from . import writer
from .airline import Airline
from .airport import Airport
from .base import Base
from .change_type import ChangeType
from .change_type_enum import ChangeTypeEnum
from .code_mapper import CodeMapper
from .exception import ExceptionInstance
from .exception import ExceptionType
from .file_operation import FileOperation
from .file_operation import FileOperationAssociation
from .file_operation import FileOperationStatus
from .file_operation import FileOperationStatusEnum
from .file_operation import FileOperationStatusTransition
from .file_operation import FileOperationType
from .file_operation import FileOperationTypeEnum
from .flight_number import FlightNumber
from .history import ChangeStatus
from .history import ChangeStatusEnum
from .history import HistoryMixin
from .ignore_file import IgnoreFile
from .leg_file import LegFile
from .leg_file_scrape import LegFileScraperHistory
from .leg_identifier import LegIdentifier
from .mime_type import MimeType
from .missing_member import MissingMember
from .ofp_version import OFPVersion
from .origin_date import OriginDate
from .os_walk import OSWalk
from .path_flavor import PathFlavor
from .path_flavor import PathFlavorEnum
from .regex import Regex
from .required_member import RequiredMember
from .schema import Schema
from .scraper import FunctionStep
from .scraper import ObjectCreator
from .scraper import ObjectCreatorEnum
from .scraper import ObjectStep
from .scraper import RegexStep
from .scraper import SchemaStep
from .scraper import Scraper
from .scraper import ScraperStep
from .scraper import ScraperStepType
from .scraper import ScraperStepTypeEnum
from .user import BotUserEnum
from .user import User
from .user import UserType
from .user import UserTypeEnum
from .zip_spec import ZipSpec

# Add *History classes to namespace.
FileOperationHistory = FileOperation._history_class

def get_models():
    """
    Return name mapping of all mapper classes, registered.
    """
    sorted_mappers = sorted(
        Base.registry.mappers,
        key = lambda mapper: mapper.class_.__name__
    )
    return {
        mapper.class_.__name__: mapper.class_
        for mapper in sorted_mappers
    }

def get_model_by_table_name(name):
    for cls in Base.__subclasses__():
        if hasattr(cls, '__tablename__') and cls.__tablename__ == name:
            return cls

def get_references(model):
    for cls in Base.__subclasses__():
        for fk in cls.__table__.foreign_keys:
            if fk.column.table.name == model.__tablename__:
                yield (cls, fk)

# Need model before adding this.
_LegIdentifier = aliased(LegIdentifier)

# Relationship of files that matched under a LegIdentifier object.
LegIdentifier.matching_files = relationship(
    LegFile,
    primaryjoin = (
        sa.and_(
            LegIdentifier.airline_id == remote(_LegIdentifier.airline_id),
            LegIdentifier.flight_number_id == remote(_LegIdentifier.flight_number_id),
            LegIdentifier.origin_date_id == remote(_LegIdentifier.origin_date_id),
            LegIdentifier.departure_airport_id == remote(_LegIdentifier.departure_airport_id),
            LegIdentifier.destination_airport_id == remote(_LegIdentifier.destination_airport_id),
            sa.or_(
                # OFP versions are exactly the same or both null.
                LegIdentifier.ofp_version_id == remote(_LegIdentifier.ofp_version_id),
                sa.and_(
                    LegIdentifier.ofp_version_id == None,
                    remote(_LegIdentifier.ofp_version_id) == None,
                ),
            ),

            LegFile.leg_identifier_id == remote(_LegIdentifier.id),
        )
    ),
    order_by = LegFile.is_zipfile,
    viewonly = True,
)

# Table rows backed enums.
enums = [
    ChangeStatusEnum,
    ChangeTypeEnum,
    FileOperationStatusEnum,
    FileOperationTypeEnum,
    ObjectCreatorEnum,
    PathFlavorEnum,
    ScraperStepTypeEnum,
    UserTypeEnum,
]

model_enum_pairs = [(eval(enum.__model__), enum) for enum in enums]
