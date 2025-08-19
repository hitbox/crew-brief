import sqlalchemy as sa

class ByMixin:
    """
    Mixin providing methods to get instance by unique attributes.
    """

    @classmethod
    def by_name(cls, session, name):
        """
        Get one OSWalk object from name or raise.
        """
        try:
            return session.execute(sa.select(cls).where(cls.name == name)).scalar_one()
        except sa.exc.NoResultFound as e:
            raise ValueError(f'{cls.__name__} name not found: {name}')
