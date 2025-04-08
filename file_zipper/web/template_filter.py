def init_app(app):

    @app.template_filter('thousands')
    def format_thousands(value):
        return f'{value:,}'

    app.jinja_env.filters['thousands'] = format_thousands
