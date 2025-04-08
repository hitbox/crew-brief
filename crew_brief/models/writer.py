import os
import shutil

from abc import ABC
from abc import abstractmethod
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
from zipfile import ZipInfo


class Writer(ABC):

    @abstractmethod
    def write(self, context, workbook, zip_path):
        """
        """


class NullWriter(Writer):
    """
    Do nothing writer.
    """

    def write(self, context, data, zip_path):
        pass


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
        Replace zip_path with updated ZIP having member_data as formatted
        self.member_name, while preserving file metadata.

        :param context: Dict with runtime data for formatting member names.
        :param member_data: Data to write to ZIP.
        :param zip_path: Path to the ZIP file being modified.
        """
        member_name = self.member_name.format(**context)

        # Preserve original ZIP metadata
        original_stat = os.stat(zip_path)

        with (
            ZipFile(zip_path, 'r') as src_zip,
            NamedTemporaryFile(delete=False, suffix='.zip') as temp_file,
            ZipFile(temp_file, 'w') as dst_zip,
        ):
            # Copy all files except the one being replaced
            for item in src_zip.infolist():
                if item.filename != member_name:
                    dst_zip.writestr(
                        item,
                        src_zip.read(item.filename),
                        compress_type = item.compress_type,
                    )
                    # Preserve metadata
                    dst_info = dst_zip.getinfo(item.filename)
                    # Preserve modified time
                    dst_info.date_time = item.date_time

            # Add the updated member with the current timestamp
            new_info = ZipInfo(member_name)
            # Preserve original timestamp
            new_info.date_time = item.date_time
            dst_zip.writestr(new_info, member_data)

        # Copy file status from original to temp file.
        shutil.copystat(zip_path, temp_file.name)

        # Update access and modified times.
        os.utime(temp_file.name)

        # Replace the original ZIP file.
        shutil.move(temp_file.name, zip_path)
