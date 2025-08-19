import sqlalchemy as sa

from functools import wraps

from .model import FileOperationType

registry = {}

def register(operation_type_name):
    """
    Decorator to register function in file operations registry.
    """
    def decorator(fn):
        registry[operation_type_name] = wrapper
        return fn
    return decorator

def raise_for_missing(session):
    """
    Validate registered file operation types exist in the database.
    """
    existing = {optype.name for optype in session.scalars(sa.select(FileOperationType))}

    registered = set(registery.keys())

    missing = registered - existing
    if missing:
        raise RuntimeError(
            f'Database is missing registered file operations {missing}')
