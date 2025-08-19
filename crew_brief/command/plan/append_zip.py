import datetime
import logging

from itertools import groupby
from itertools import product
from operator import attrgetter

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from crew_brief import configlib
from crew_brief.model import FileOperation
from crew_brief.model import FileOperationStatusEnum
from crew_brief.model import FileOperationTypeEnum
from crew_brief.model import User
from crew_brief.query import select_leg_identifiers_with_partial

logger = logging.getLogger(__name__)

def add_parser(parsers):
    """
    Add plan sub-commands.
    """
    parser = parsers.add_parser(
        'append_zip',
        description = plan_append_zip_command.__doc__,
        help = plan_append_zip_command.__doc__,
    )
    parser.add_argument(
        '--commit',
        action = 'store_true',
        help = 'Commit changes.',
    )
    parser.add_argument(
        '--echo',
        action = 'store_true',
        help = 'Echo SQL.',
    )
    parser.add_argument(
        '--batch',
        type = int,
        default = 1000,
        help = 'Batch commit size.',
    )
    parser.add_argument(
        '--limit',
        type = int,
        help = 'Limit number of file operations to create.',
    )
    parser.add_argument(
        '--enable',
        action = 'store_true',
        help = 'Create ZIP_APPEND file operations as enabled.',
    )
    configlib.add_config_option(parser)
    parser.set_defaults(func=plan_append_zip_command)

def plan_append_zip_command(args):
    """
    Plan new file operations to append files to ZIPs.
    """
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    engine = create_engine(database_uri, echo=args.echo)
    with Session(engine) as session:
        # Initialize current_user.
        stmt = select(User).where(User.username == 'planbot')
        session.info['current_user'] = session.scalars(stmt).one()

        # Attribute getter for attribute that tells us for sure the file is a zip.
        by_is_really_zip = attrgetter('is_really_zip')

        zip_append = FileOperationTypeEnum.ZIP_APPEND.db_object(session)

        created_status = FileOperationStatusEnum.CREATED.db_object(session)

        batch = []
        ncreated = 0
        stmt = select_leg_identifiers_with_partial()
        for leg_identifier in session.scalars(stmt).yield_per(500):
            # Group matching files into ZIPs and not-ZIPs
            grouped_is_zip = sorted(leg_identifier.matching_files, key=by_is_really_zip)
            grouped_is_zip = groupby(grouped_is_zip, key=by_is_really_zip)
            grouped_is_zip = {key: list(leg_files) for key, leg_files in grouped_is_zip}

            # Pair them as ZIP file, not-ZIP file.
            pairs = product(grouped_is_zip[True], grouped_is_zip[False])
            for zip_file, append_file in pairs:
                # Skip if operation exists for files.
                # TODO
                # - This did not filter out existing operations.
                # - Check again after making FileOperation.files relationship.
                stmt = (
                    select(FileOperation)
                    .where(
                        FileOperation.target_file == append_file,
                        FileOperation.leg_file == zip_file,
                        FileOperation.operation_type == zip_append,
                    )
                )
                existing_file_operation = session.scalars(stmt).first()
                if existing_file_operation:
                    continue

                # Create file operation.
                file_operation = FileOperation(
                    # Append target_file to the zip_file.
                    target_file = append_file,
                    leg_file = zip_file,
                    operation_type = zip_append,
                    status = created_status,
                    enabled_at = datetime.datetime.now() if args.enable else None,
                )
                batch.append(file_operation)
                ncreated += 1
                if args.limit and ncreated == args.limit:
                    break
                if len(batch) == args.batch:
                    session.add_all(batch)
                    session.flush()
                    batch.clear()

            if args.limit and ncreated == args.limit:
                break

        if batch:
            session.add_all(batch)
            session.flush()

        if args.commit:
            session.commit()
