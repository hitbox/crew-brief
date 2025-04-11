import os

from abc import ABC
from abc import abstractmethod

class Archive(ABC):
    """
    Load and save some kind of archive used to avoid reprocessing files.
    """

    @abstractmethod
    def check(self, path):
        """
        Return bool that path exists in archive.
        """

    @abstractmethod
    def save(self, path):
        """
        Save path as archived.
        """


class NullArchive(Archive):
    """
    Archive that always checks false and does nothing for save.
    """

    def check(self, check_path):
        return False

    def save(self, save_path):
        pass


class PathArchive(Archive):
    """
    Maintain a set and a file of paths for checking if they've
    already been processed.
    """

    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.saved_paths = set()
        self.load_paths()

    def load_paths(self):
        if os.path.exists(self.archive_path):
            with open(self.archive_path) as archive_file:
                for saved_path in archive_file:
                    self.saved_paths.add(saved_path.strip())

    def check(self, check_path):
        return check_path in self.saved_paths

    def save(self, save_path):
        if save_path not in self.saved_paths:
            with open(self.archive_path, 'a') as archive_file:
                archive_file.write(save_path + '\n')
            self.saved_paths.add(save_path)
