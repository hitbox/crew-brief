import os

from datetime import datetime
from datetime import timezone

from crew_brief.business import update_for_zip_spec
from crew_brief.model import ZipSpec
from crew_brief.query import select_incomplete_leg_files
from crew_brief.util import Batch

def update_required_members(session, spec_name, batch_size=100, yield_per=50):
    """
    Update LegFile objects for their status regarding how complete they are.
    """
    # Get ZipSpec object by name.
    zip_spec = ZipSpec.by_name(session, spec_name)

    # Select incomplete ZIP files.
    incomplete_leg_files = session.scalars(select_incomplete_leg_files())

    # NOTE
    # - timezone aware datetimes here but the database is naive at the moment.

    batch = Batch(batch_size)
    for leg_file in incomplete_leg_files.yield_per(yield_per):
        try:
            # Only update if file exists and has changed since last mtime capture.
            stat = os.stat(leg_file.path)
            if leg_file.mtime is not None and stat.st_mtime <= leg_file.mtime:
                continue

            # Update LegFile for ZipSpec.
            update_for_zip_spec(session, leg_file, zip_spec)
        except FileNotFoundError:
            leg_file.not_exists_at = datetime.now(timezone.utc)
            continue

        # Update mtime and completeness check timestamps.
        leg_file.mtime = stat.st_mtime
        leg_file.check_complete_at = datetime.now(timezone.utc)
        # Append work and commit for batch size.
        batch.append(session, leg_file)

    batch.finalize(session)
