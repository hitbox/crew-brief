import glob
import json
import os
import re
import zipfile

from abc import ABC
from abc import abstractmethod

from .path_data import PathData

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
            yield PathData(path)


class WalkMixin:

    def _walk_generator(self, top):
        return os.walk(top, **self.walk_args)

    def _paths(self, subs):
        top = self.top.format(**subs)
        generator = self._walk_generator(top)
        for dirpath, dirnames, filenames in generator:
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                yield path


class WalkFilesSource(Source, WalkMixin):
    """
    Generate paths with os.walk.
    """

    def __init__(self, top, walk_args=None):
        """
        :param top: Top dir argument for os.walk.
        """
        self.top = top
        if walk_args is None:
            walk_args = {}
        self.walk_args = walk_args

    def paths(self, subs):
        """
        :param subs:
            Dict of substitutions to make available to path string.
        """
        for path in self._paths(subs):
            yield PathData(path)


class ZipMemberWalker(Source, WalkMixin):
    """
    Recursively walks the filesystem to find zip files. For each zip file
    found, opens it and yields members whose names match a given regex.

    Only the top-level entries inside each zip file are considered
    (non-recursive).
    """

    def __init__(self, top, member_re, walk_args=None, loader=None):
        """
        :param top:
            Walk from root at `top` for zip files.
        :param member_re:
            String or regex that matches the members of the zip files.
        :param walk_args:
            Additional arguments to pass to `os.walk`.
        :param loader:
            Loads the matching member file.
        """
        self.top = top

        if isinstance(member_re, str):
            member_re = re.compile(member_re)
        self.member_re = member_re

        if walk_args is None:
            walk_args = {}
        self.walk_args = walk_args

        if loader is None:
            loader = json.load
        self.loader = loader

    def paths(self, subs):
        for path in self._paths(subs):
            # Skip non-ZIP files
            if not zipfile.is_zipfile(path):
                continue
            # Yield members of ZIP that match regex.
            with zipfile.ZipFile(path, 'r') as zip_file:
                for member_name in zip_file.namelist():
                    # Skip not matching.
                    if not self.member_re.match(member_name):
                        continue
                    # Load data from matching member.
                    with zip_file.open(member_name) as member_file:
                        member_data = self.loader(member_file)
                    yield PathData(path, subpath=member_name, data=member_data)
