from .index import Index


def register_routes(app):
	index_view = Index.as_view("index")
	app.add_url_rule("/", view_func=index_view)
	app.add_url_rule("/index", view_func=index_view)