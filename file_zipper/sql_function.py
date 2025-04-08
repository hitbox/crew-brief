import datetime
import sqlite3

import sqlalchemy as sa

def str_to_date(date_str, format_str):
    try:
        return datetime.datetime.strptime(date_str, format_str).date()
    except (TypeError, ValueError):
        return None

def register_sqlite_functions(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        dbapi_connection.create_function('STR_TO_DATE', 2, str_to_date)

def register_functions(dbapi_connection, connection_record):
    register_sqlite_functions(dbapi_connection, connection_record)
