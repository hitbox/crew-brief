import copy
import io
import json
import logging
import re

from abc import ABC
from abc import abstractmethod
from zipfile import ZipFile

from crew_brief.paths import setdefault_for_base_path
from crew_brief.schema import UserEventsSchema
from crew_brief.workbook import build_workbook_for_member

class Process(ABC):
    """
    Abstract class requiring a run method.
    """

    @abstractmethod
    def run(self):
        pass


class UpdateUserFriendlyProcess(Process):
    """
    Generate a user-friendly Excel file from JSON data stored in ZIP files and
    update the ZIP with the newly created Excel file.
    """

    member_schema_class = UserEventsSchema

    def __init__(
        self,
        sources,
        member_re,
        writer,
        archive,
        path_data_re = None,
    ):
        """
        :param sources:
            List of source objects that generate paths to zip files.
        :param member_re:
            Regex to match a JSON file, member of the zip files.
        :param writer:
            Writer object handles writing Excel workbook created from the
            matching member's JSON data.
        :param archive:
            Archive object that saves paths to avoid reprocessing.
        :param path_data_re = None:
            Regex with named captures for data embedded into the paths.
        """
        self.sources = sources
        if isinstance(member_re, str):
            member_re = re.compile(member_re)
        self.member_re = member_re
        self.writer = writer
        self.archive = archive
        if isinstance(path_data_re, str):
            path_data_re = re.compile(path_data_re)
        self.path_data_re = path_data_re

    def _generate_paths(self, subs):
        """
        Generator for all paths from all sources.
        """
        for source in self.sources:
            for path in source.paths(subs):
                yield path

    def run(self, subs):
        """
        :param subs:
            Substitution dict passed to the path generator and the base context
            for each path.
        """
        logger = logging.getLogger('crew_brief')

        # Schema for ZIP member JSON.
        member_schema = self.member_schema_class()

        # Excel workbook builder.
        workbook_builder = build_workbook_for_member

        # Process members of ZIP files for each generated path.
        for zip_path in self._generate_paths(subs):
            # Check if zip path has already been processed.
            if self.archive.check(zip_path):
                continue

            # Start context for each path from given sub(stitutes).
            context = copy.deepcopy(subs)

            # Add useful path parts from os.path processing.
            setdefault_for_base_path(context, zip_path)

            # If configured, update context data from filename regex.
            if self.path_data_re:
                path_match = self.path_data_re.match(zip_path)
                if path_match:
                    context.update(path_match.groupdict())

            # Open ZIP, look for member, create Excel, write back to ZIP and
            # save path.
            with ZipFile(zip_path, 'r') as zip_file:
                for member_name in zip_file.namelist():
                    if self.member_re.match(member_name):
                        # Parse member as JSON
                        with zip_file.open(member_name) as member_file:
                            member_data = json.load(member_file)

                        # Convert types, keeping original.
                        member_data_typed = member_schema.load(member_data)

                        # Build in-memory Excel workbook.
                        wb = workbook_builder(member_data, member_data_typed)
                        with io.BytesIO() as excel_stream:
                            wb.save(excel_stream)
                            member_data = excel_stream.getvalue()

                        # Call configured writer with new workbook data.
                        self.writer.write(context, member_data, zip_path)

                        # Save path to archive.
                        self.archive.save(zip_path)

                        logger.info('processed:%s', zip_path)

                        # Break looping members. May have to support multiple
                        # matches later.
                        break
