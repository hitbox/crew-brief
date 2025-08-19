from sqlaclhemy.sql import expression
from sqlalchemy import DateTime
from sqlalchemy.ext.compiler import compiles

class server_utc_now(expression.FunctionElement):
    """
    Render dialect specific function to get the current UTC time from the
    database.
    """
    # Return type.
    type = DateTime(timezone=True)

    # Mark safe to cache.
    inherit_cache = True


@compiles(server_utc_now, 'postgresql')
def pg_utc_now(element, compiler, **kw):
    return "CURRENT_TIMESTAMP AT TIME ZONE 'UTC'"

@compiles(server_utc_now, 'mysql')
def mysql_utc_now(element, compiler, **kw):
    return 'CURRENT_TIMESTAMP'

@compiles(server_utc_now, 'sqlite')
def sqlite_utc_now(element, compiler, **kw):
    return "(datetime('now'))"

@compiles(server_utc_now)
def default_utc_now(element, compiler, **kw):
    return 'NOW()'
