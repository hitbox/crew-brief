import os

from abc import ABC
from abc import abstractmethod

class Source(ABC):

    @abstractmethod
    def paths(self, subs):
        """
        :param subs: Dict of path string substitutions.
        """


class WalkFilesSource(Source):
    """
    Generate paths with os.walk.
    """

    def __init__(
        self,
        top,
        normpath = False,
        topdown = True,
        onerror = None,
        followlinks = False,
    ):
        """
        :param top: Top dir argument for os.walk.
        :param normpath: Normalize path before yielding.
        :param topdown: os.walk argument
        :param onerror: os.walk argument
        :param followlinks: os.walk argument
        """
        self.normpath = normpath
        self.top = top
        self.topdown = topdown
        self.onerror = onerror
        self.followlinks = followlinks

    def _walk_generator(self, top):
        return os.walk(top, self.topdown, self.onerror, self.followlinks)

    def paths(self, subs):
        """
        :param subs:
            Dict of substitutions to make available to path string.
        """
        top = self.top.format(**subs)
        generator = self._walk_generator(top)
        for dirpath, dirnames, filenames in generator:
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if self.normpath:
                    path = os.path.normpath(path)
                yield path
