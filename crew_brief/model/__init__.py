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
from .attribute_sort import AttributeSort
from .base import Base
from .change_type_enum import ChangeTypeEnum
from .code_mapper import CodeMapper
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
from .leg_file_scrape import LegFileScrape
from .leg_file_scrape import LegFileScrapeStatus
from .leg_file_scrape import LegFileScrapeStatusEnum
from .leg_identifier import LegIdentifier
from .mime_type import MimeType
from .missing_member import MissingMember
from .ofp_version import OFPVersion
from .origin_date import OriginDate
from .os_walk import OSWalk
from .path_flavor import PathFlavor
from .regex import Regex
from .required_member import RequiredMember
from .schema import Schema
from .scraper import Scraper
from .scraper import ScraperStep
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
                LegIdentifier.ofp_version == remote(_LegIdentifier.ofp_version),
                sa.and_(
                    LegIdentifier.ofp_version == None,
                    remote(_LegIdentifier.ofp_version) == None,
                ),
            ),

            LegFile.leg_identifier_id == remote(_LegIdentifier.id),
        )
    ),
    order_by = LegFile.is_zipfile,
    viewonly = True,
)
