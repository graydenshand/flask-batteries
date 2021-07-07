from .index import index_view


def register_routes(app):
    app.add_url_rule("/", view_func=index_view)
    app.add_url_rule("/index", view_func=index_view)
