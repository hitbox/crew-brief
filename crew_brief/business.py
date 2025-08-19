import datetime
import logging
import os
import zipfile

from .model import MissingMember

logger = logging.getLogger(__name__)

def update_for_zip_spec(session, leg_file, zip_spec):
    """
    Update the missing_members list according to the required names in the
    zip_spec.
    """
    # Get member names from zip
    with zipfile.ZipFile(leg_file.path, 'r') as zip_file:
        names = set(name.lower() for name in zip_file.namelist())

    # Update completed or missing.
    missing_required_members = [
        required_member for required_member in zip_spec.required_members
        if required_member.filename.lower() not in names
    ]
    if not missing_required_members:
        # Mark incomplete zip leg_file as complete, now.
        leg_file.complete_at = datetime.datetime.now()
        logger.info('Marked complete: %s', os.path.normpath(leg_file.path))
    elif leg_file.missing_members != missing_required_members:
        # Update missing members.
        leg_file.missing_members = [
            MissingMember(
                required_member = required_member,
            )
            for required_member in missing_required_members
        ]
        session.add_all(leg_file.missing_members)
        logger.info('Updated missing members %s', os.path.normpath(leg_file.path))
