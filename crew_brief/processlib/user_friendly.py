import copy
import io
import json
import logging
import re

from abc import ABC
from abc import abstractmethod
from zipfile import ZipFile

from crew_brief import configlib
from crew_brief.models import eval_context
from crew_brief.paths import setdefault_for_base_path
from crew_brief.schema import UserEventsSchema
from crew_brief.workbook import build_workbook_for_member

from .base import Process

class UpdateUserFriendlyProcess(Process):
    """
    Generate a user-friendly Excel file from JSON data stored in ZIP files and
    update the ZIP with the newly created Excel file.
    """

    member_schema_class = UserEventsSchema

    @classmethod
    def from_config(cls, cp, name, process_section):
        sources = {}
        archives = {}
        writers = {}
        member_regexes = {}
        path_data_regexes = {}

        # Required regex to match member for JSON file.
        member_re_name = process_section['member_re']
        if member_re_name not in member_regexes:
            member_re_section = cp['zip_member_re.' + member_re_name]
            member_re = compile_regex(member_re_section['member_re'])
            member_regexes[member_re_name] = member_re
        member_re = member_regexes[member_re_name]

        # Required writer key to section.
        writer_name = process_section['writer']
        if writer_name not in writers:
            # Update writer named dict.
            writer_section = cp['writer.' + writer_name]
            writers[writer_name] = configlib.instance_section(writer_section, eval_context)
        writer = writers[writer_name]

        # Optional path_data_re regex.
        if 'path_data' in process_section:
            path_data_name = process_section['path_data']
            if path_data_name not in path_data_regexes:
                path_data_section = cp['path_data.' + path_data_name]
                path_data_re = compile_regex(path_data_section['path_data_re'])
                path_data_regexes[path_data_name] = path_data_re
            path_data_re = path_data_regexes[path_data_name]
        else:
            path_data_re = None

        # List of source objects for this process.
        sources_list = []
        for source_name in configlib.human_split(process_section['sources']):
            if source_name not in sources:
                # Update named sources dict.
                source_section = cp['source.' + source_name]
                sources[source_name] = configlib.instance_section(source_section, eval_context)
            # Add source for process.
            sources_list.append(sources[source_name])

        # Archive after processing object.
        archive_name = process_section['archive']
        if archive_name not in archives:
            # Update named archive dict.
            archive_section = cp['archive.' + archive_name]
            archives[archive_name] = configlib.instance_section(archive_section, eval_context)
        archive = archives[archive_name]

        return cls(
            sources = sources_list,
            member_re = member_re,
            writer = writer,
            archive = archive,
            path_data_re = path_data_re,
        )

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
            member_re = compile_regex(member_re)
        self.member_re = member_re
        self.writer = writer
        self.archive = archive
        if isinstance(path_data_re, str):
            path_data_re = compile_regex(path_data_re)
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


def compile_regex(pattern):
    return re.compile(pattern, re.VERBOSE)
