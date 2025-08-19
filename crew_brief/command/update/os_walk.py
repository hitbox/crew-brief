import sqlalchemy as sa

from sqlalchemy.orm import Session

from crew_brief import configlib
from crew_brief.model import LegFile
from crew_brief.model import OSWalk

def add_parser(parsers):
    parser = parsers.add_parser('os_walk', help=update_os_walk.__doc__)
    configlib.add_config_option(parser)
    parser.set_defaults(func=update_os_walk)

def update_os_walk(args):
    """
    Ignore existing and update all LegFile objects for their path and os_walk
    attributes.
    """
    # This mainly exists to update LegFile objects after adding OSWalk objects
    # as os_walk attributes.

    # Read Python config file and get database uri.
    config = configlib.pyfile_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')

    engine = sa.create_engine(database_uri)
    with Session(engine) as session:
        # Verify names and get OSWalk objects from database.
        walkers = session.scalars(sa.select(OSWalk)).all()

        # Get mapping for existing paths.
        existing_paths = {leg_file.path: leg_file for leg_file in session.scalars(sa.select(LegFile))}

        for walker in walkers:
            for path in walker.walk_filenames():
                # Update existing or create new.
                if path in existing_paths:
                    leg_file = existing_paths[path]
                    leg_file.os_walk = walker
                else:
                    leg_file = LegFile(path=path, os_walk=walker)
                    session.add(leg_file)

        session.commit()
