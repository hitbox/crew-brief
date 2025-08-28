def init_app(app):
    @app.template_filter('as_list')
    def as_list(value):
        """
        Template filter to ensure a list. some_var|as_list -> always a list.
        """
        if not isinstance(value, (list, set, tuple)):
            value = [value]
        return value
