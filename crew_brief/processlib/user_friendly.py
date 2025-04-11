import copy
import logging
import re

from abc import ABC
from abc import abstractmethod
from zipfile import ZipFile

from crew_brief import configlib
from crew_brief import shapers
from crew_brief.model import eval_context
from crew_brief.path import setdefault_for_base_path
from crew_brief.schema import UserEventsSchema
from crew_brief.workbook import build_workbook_for_member

from .base import Process

class UpdateUserFriendlyProcess(Process):
    """
    Generate a user-friendly Excel file from JSON data stored in ZIP files and
    update the ZIP with the newly created Excel file.
    """

    member_schema_class = UserEventsSchema

    def __init__(
        self,
        sources,
        writer,
        archive,
        output,
        path_data_re = None,
        styling = None,
    ):
        """
        :param sources:
            List of source objects that generate paths to zip files.
        :param writer:
            Writer object handles writing Excel workbook created from the
            matching member's JSON data.
        :param archive:
            Archive object that saves paths to avoid reprocessing.
        :param path_data_re = None:
            Regex with named captures for data embedded into the paths.
        :param output:
            Object that writes output.
        :param styling:
            Styling lookup object.
        """
        self.sources = sources
        self.writer = writer
        self.archive = archive
        if isinstance(path_data_re, str):
            path_data_re = compile_regex(path_data_re)
        self.path_data_re = path_data_re
        self.output = output
        self.styling = styling

    def _generate_paths(self, subs):
        """
        Generator for all paths from all sources.
        """
        for source in self.sources:
            for path in source.paths(subs):
                yield path

    def method_to_yield_the_userevents_memebers(self):
        raise NotImplementedError

    def run(self, subs):
        """
        :param subs:
            Substitution dict passed to the path generator and the base context
            for each path.
        """
        logger = logging.getLogger('crew_brief')

        # Schema for ZIP member JSON.
        member_schema = self.member_schema_class()

        # Process members of ZIP files for each generated path.
        for path_data in self._generate_paths(subs):
            # Check if zip path has already been processed.
            if self.archive.check(path_data.path):
                continue

            # Start context for each path from given sub(stitutes).
            context = copy.deepcopy(subs)

            # Add useful path parts from os.path processing.
            setdefault_for_base_path(context, path_data.path)

            # If configured, update context data from filename regex.
            if self.path_data_re:
                path_match = self.path_data_re.match(path_data.path)
                if path_match:
                    context.update(path_match.groupdict())

            # Convert types, keeping original.
            member_data_typed = member_schema.load(path_data.data)

            # Build in-memory Excel workbook.
            # TODO
            # - path_data.data seems to be member_data_typed

            shaper = shapers.MemberDataShaper()
            shaper(member_data_typed)
            output_data = self.output(path_data.data, member_data_typed)

            # Call configured writer with new workbook data.
            self.writer.write(context, output_data, path_data.path)

            # Save path to archive.
            self.archive.save(path_data.path)

            logger.info('processed:%s', path_data.path)


def compile_regex(pattern):
    return re.compile(pattern, re.VERBOSE)
