from flask import current_app, url_for

def static_url_for(path):
	if current_app.config['USE_WEBPACK_DEV_SERVER']:
		return f"http://localhost:3000/static/{path}"
	else:
		return url_for('static', filename=path)