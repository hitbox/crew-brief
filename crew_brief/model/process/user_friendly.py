import copy
import logging
import re

from crew_brief import shapers
from crew_brief.path import setdefault_for_base_path

from .base import Process
from .mixin import PathMixin

class UpdateUserFriendlyProcess(Process, PathMixin):
    """
    Generate a user-friendly Excel file from JSON data stored in ZIP files and
    update the ZIP with the newly created Excel file.
    """

    def __init__(
        self,
        sources,
        schema,
        writer,
        archive,
        output,
        path_data_re = None,
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
        """
        self.sources = sources
        self.schema = schema
        self.writer = writer
        self.archive = archive
        if isinstance(path_data_re, str):
            path_data_re = compile_regex(path_data_re)
        self.path_data_re = path_data_re
        self.output = output
        self.shaper = shapers.MemberDataShaper()

    def run(self, subs):
        """
        :param subs:
            Substitution dict passed to the path generator and the base context
            for each path.
        """
        logger = logging.getLogger('crew_brief')

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
            member_data_typed = self.schema.load(path_data.data)

            # Reshape typed data.
            self.shaper(member_data_typed)

            # Build in-memory Excel workbook.
            output_data = self.output(path_data.data, member_data_typed)

            # Call configured writer with new workbook data.
            self.writer.write(context, output_data, path_data.path)

            # Save path to archive.
            self.archive.save(path_data.path)

            logger.info('processed:%s', path_data.path)


def compile_regex(pattern):
    return re.compile(pattern, re.VERBOSE)
