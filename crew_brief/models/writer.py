import shutil

from abc import ABC
from abc import abstractmethod
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

class Writer(ABC):

    @abstractmethod
    def write(self, context, workbook, zip_path):
        """
        """


class FileWriter(Writer):
    """
    Write data to file.
    """

    def __init__(self, path):
        self.path = path

    def write(self, context, data, zip_path):
        path = self.path.format(**context)
        with open(path, 'wb') as output_file:
            output_file.write(data)


class ZipFileWriter(Writer):

    def __init__(self, member_name):
        self.member_name = member_name

    def write(self, context, member_data, zip_path):
        """
        Replace zip_path with update ZIP having member_data as formatted
        self.member_name.

        :param context:
            Context dict of things picked up from processing paths, filenames,
            and useful runtime data like named dates.
        :param member_data:
            Data to write to ZIP member.
        """
        member_name = self.member_name.format(**context)

        # TODO
        # - Keep original file metadata.

        with (
            # Source zip file to read from.
            ZipFile(zip_path, 'r') as src_zip,
            # Temporary file on disk to write zip output to.
            NamedTemporaryFile(delete=False, suffix='.zip') as temp_file,
            # Open temp file to write filtered source.
            ZipFile(temp_file, 'w') as dst_zip,
        ):
            # Keep other files, writing to temp.
            for item in src_zip.infolist():
                if item.filename != member_name:
                    dst_zip.writestr(item, src_zip.read(item.filename))
            # Append new data.
            dst_zip.writestr(member_name, member_data)

        # Replace/overwrite with updated ZIP.
        shutil.move(temp_file.name, zip_path)
