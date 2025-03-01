import glob
import os

from abc import ABC
from abc import abstractmethod

class Source(ABC):

    @abstractmethod
    def paths(self, subs):
        """
        :param subs: Dict of path string substitutions.
        """


class GlobSource(Source):

    def __init__(
        self,
        pathname,
        root_dir = None,
        dir_fd = None,
        recursive = False,
        include_hidden = False,
        iterative = True,
        join_root = True,
        normpath = True,
    ):
        """
        Glob function arguments:
        :param pathname:
        :param root_dir:
        :param dir_fd:
        :param recursive:
        :param include_hidden:

        :param iterative: True to use iglob.
        :param join_root: True to join root_dir to results.
        """
        self.pathname = pathname
        self.root_dir = root_dir
        self.dir_fd = dir_fd
        self.recursive = recursive
        self.include_hidden = include_hidden
        self.iterative = iterative
        self.join_root = join_root
        self.normpath = normpath

    def _glob(self, pathname):
        if self.iterative:
            globfunc = glob.iglob
        else:
            globfunc = glob.glob

        kwargs = {
            'root_dir': self.root_dir,
            'dir_fd': self.dir_fd,
            'recursive': self.recursive,
            'include_hidden': self.include_hidden,
        }
        return globfunc(pathname, **kwargs)

    def paths(self, subs):
        """
        Generate paths from patterns.
        """
        pathname = self.pathname.format(**subs)
        for path in self._glob(pathname):
            if self.join_root and self.root_dir is not None:
                path = os.path.join(self.root_dir, path)
            if self.normpath:
                path = os.path.normpath(path)
            yield path


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
