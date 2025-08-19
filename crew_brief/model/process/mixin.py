class PathMixin:

    def _generate_paths(self, subs, normalize=None):
        """
        Generator for all paths from all sources.
        """
        for source in self.sources:
            for path_data in source.paths(subs):
                if normalize:
                    path_data.path = normalize(path_data.path)
                yield path_data
