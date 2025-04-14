class ItemMixin:
    """
    Mixin dict item access for instances.
    """

    __order__ = None
    __data_attr__ = None

    @property
    def __data(self):
        if self.__data_attr__:
            return getattr(self, self.__data_attr__)
        return self

    def __getitem__(self, key):
        return getattr(self.__data, key)

    def __setitem__(self, key, value):
        setattr(self.__data, key, value)

    def __contains__(self, key):
        return hasattr(self.__data, key)

    def __iter__(self):
        return self.keys()

    def __len__(self):
        return sum(1 for _ in self.keys())

    def get(self, key, default=None):
        return getattr(self.__data, key, default)

    def items(self):
        for key in dir(self.__data):
            if key.startswith('_'):
                continue
            val = getattr(self.__data, key)
            if not callable(val):
                yield (key, val)

    def keys(self):
        return (key for key, _ in self.items())

    def values(self):
        return (val for _, val in self.items())
