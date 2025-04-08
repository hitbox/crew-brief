from flask import Blueprint

from file_zipper.model import ExcludedPath
from file_zipper.model import FileType
from file_zipper.model import Glob
from file_zipper.model import Path
from file_zipper.model import Regex
from file_zipper.model import Schema
from file_zipper.web.extension import db

model_list = [
    ExcludedPath,
    FileType,
    Glob,
    Path,
    Regex,
    Schema,
]

statements = {
    Path: db.select(Path).order_by(Path.path),
}

def init_context_processor(app):
    @app.context_processor
    def context_processor():
        return {
            'models': model_list,
        }
