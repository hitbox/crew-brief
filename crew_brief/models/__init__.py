from .archive import PathArchive
from .source import GlobSource
from .source import WalkFilesSource
from .writer import FileWriter
from .writer import ZipFileWriter

eval_context = {
    'FileWriter': FileWriter,
    'GlobSource': GlobSource,
    'PathArchive': PathArchive,
    'WalkFilesSource': WalkFilesSource,
    'ZipFileWriter': ZipFileWriter,
}
