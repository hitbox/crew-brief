from operator import attrgetter

import sqlalchemy as sa

class InstanceMixin:
    """
    Mixin method to get instance by one of the model's attributes.
    """

    @classmethod
    def instance_cache(cls, session):
        """
        Return dict mapping of instance primary keys to instances.
        """
        mapper = sa.inspect(cls)
        pk = attrgetter(*(col.name for col in mapper.primary_key))
        return {pk(inst): inst for inst in session.scalars(sa.select(cls))}

    @classmethod
    def instances_by_attr(cls, session, attr):
        return {getattr(inst, attr): inst for inst in session.scalars(sa.select(cls))}
