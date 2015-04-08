import strftime


def init_app(app):
    app.jinja_env.filters['strftime'] = strftime.strftime
