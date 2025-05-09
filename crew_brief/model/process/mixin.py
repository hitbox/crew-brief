class PathMixin:

    def _generate_paths(self, subs):
        """
        Generator for all paths from all sources.
        """
        for source in self.sources:
            for path in source.paths(subs):
                yield path
