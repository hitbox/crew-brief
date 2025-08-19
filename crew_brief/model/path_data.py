class PathData:
    """
    Normally just a path but the object is meant to contain extra data that
    comes from descending into an archive.
    """

    def __init__(self, path, subpath=None, data=None):
        self.path = path
        self.subpath = subpath
        self.data = data
