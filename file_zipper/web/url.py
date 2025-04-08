import sqlalchemy as sa

def model_url_rule(model_class):
    """
    Generate a Flask-style URL rule string from a SQLAlchemy model's primary
    key.
    """
    table_name = model_class.__table__.name
    inspector = sa.inspect(model_class)
    pk_columns = [col.name for col in inspector.primary_key]

    # Build the route with type hints for Flask
    pk_parts = []
    for col in inspector.primary_key:
        converter = col.type.python_type.__name__.lower()
        part = f'<{converter}:{col.name}>'
        pk_parts.append(part)

    return f'/{table_name}/' + '/'.join(pk_parts)
