from operator import attrgetter

import sqlalchemy as sa

class InstanceCache:
    """
    Object used to get or create new instances that is preloaded with a cache.
    """

    def __init__(self, builder, data):
        self.builder = builder
        self.data = data

    def get_or_add(self, session, key_values):
        try:
            obj = self.data[key_values]
        except KeyError:
            obj = self.builder(key_values)
            session.add(obj)
            self.data[key_values] = obj
        return obj

    @classmethod
    def from_model(cls, session, model, *names):
        """
        Create an InstanceCache object from a model indexed by one or more attribute names.
        """
        assert hasattr(model, 'from_key_values')
        key = attrgetter(*names)
        instances = session.scalars(sa.select(model))
        instance_cache = cls(
            data = {key(inst): inst for inst in instances},
            builder = model.from_key_values,
        )
        return instance_cache
