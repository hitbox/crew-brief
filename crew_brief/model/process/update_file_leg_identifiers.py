import sqlalchemy as sa

from crew_brief.model import LegFile

from .base import Process

class UpdateFileLegIdentifier(Process):
    """
    Update file objects without a corresponding leg identifier object.
    """

    def __init__(self, database_uri, regex, schema):
        self.database_uri = database_uri
        self.regex = regex
        self.schema = schema

    def run(self, subs):
        """
        """
        engine = sa.create_engine(self.database_uri)

        with Session(engine) as session:
            stmt = sa.select(LegFile).where(LegFile.leg_identifier_id == None)
            leg_files = session.scalars(stmt)
            for leg_file in leg_files:
                print(leg_file)
