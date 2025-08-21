import sqlalchemy as sa

def seed_for_enum(session, enum_class, delete_existing=False, instance_kw=None):
    """
    Check and optionally delete for existing rows, from an enum; and create
    from enum.
    """
    if instance_kw is None:
        instance_kw = {}

    # Try to resolve model class.
    try:
        model = enum_class.get_model()
    except AttributeError as e:
        raise RuntimeError(
            f'Model argument not given and'
            f' {enum_class.__name__}.get_model() not defined.'
        ) from e

    # Checking for existing and raise or delete.
    for member in enum_class:
        existing_instance = session.get(model, member.value)
        if existing_instance:
            if not delete_existing:
                raise ValueError(f'Instances exist for {model}.')
            session.delete(existing_instance)

    # Flush changes and create new instances.
    session.flush()
    for member in enum_class:
        instance = member.db_instance(**instance_kw)
        session.add(instance)

def raise_for_exists(session, model, delete_exists=False):
    """
    Raise for existing data or delete all rows if option given.
    """
    stmt = sa.select(sa.exists().select_from(model))
    instances_exist = session.scalar(stmt)
    if instances_exist:
        # Raise if delete existing option not given.
        if not delete_exists:
            raise ValueError(
                f'Instances exist for {model}. Use --delete-exists to remove them.')

        # Delete all rows for model.
        session.execute(sa.delete(model))
