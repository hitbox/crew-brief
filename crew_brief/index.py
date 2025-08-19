import logging
import mimetypes
import os
import zipfile

import sqlalchemy as sa

from crew_brief.model import LegFile
from crew_brief.model import MimeType
from crew_brief.model import OSWalk

logger = logging.getLogger(__name__)

def index_files(session, walkers):
    """
    Save new LegFile objects from file listings.
    """
    # Get existing (seen) paths.
    existing_paths = set(session.scalars(sa.select(LegFile.path)))

    # Get existing mime type instances.
    existing_mime_types = {
        mime_type.mime: mime_type
        for mime_type in session.scalars(sa.select(MimeType))
    }

    # Save unseen paths in a set for bulk add.
    for walker in walkers:
        for path in walker.walk_filenames():
            if path not in existing_paths:
                # Guess MIME type and get or create MimeType object.
                mime, _ = mimetypes.guess_type(path)
                mime = mime or 'application/octet-stream'

                if mime not in existing_mime_types:
                    mime_type = MimeType(mime=mime)
                    session.add(mime_type)
                    existing_mime_types[mime] = mime_type
                else:
                    mime_type = existing_mime_types[mime]

                leg_file = LegFile(
                    # The new path.
                    path = path,
                    # The walker that produced it.
                    os_walk = walker,
                    # The mtime of the file.
                    mtime = os.stat(path).st_mtime,
                    # Is a ZIP file?
                    is_zipfile = zipfile.is_zipfile(path),
                    # MIME Type
                    mime_type = mime_type,
                )
                session.add(leg_file)
                logger.info('%r added %s', walker.name, path)
