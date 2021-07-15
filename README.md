*\~work in progress\~*

# Flask-Batteries

An opinionated command line tool for bootstrapping Flask applications with less boiler-plate code.

Inspired by Ruby on Rails.


## Usage
This package adds a collection of command line utilites for modifying your Flask project.

It's recommended to install this package in an isolated virtual environment. The best way to start a new project is like this:

Create a new directory to store your Flask project, and set it as your current working directory. 
```bash
mkdir app
cd app
```

Create a new virtual environment named `venv`, and activate it. 
```bash
python3 -m venv venv
source venv/bin/activate
```

Install this package, and invoke the `flask new` command which creates a scaffold for you to build your app around. 
```bash
pip install flask-batteries
flask new
```

Finally, re-activate the virtual environment (because the `flask new` command injects environment variables into your `venv/bin/activate` script), and run the app. 
```bash
source venv/bin/activate
flask run
```

Open up https://127.0.0.1:5000/ in your browser and you should see your app running.


### Commands

## Tests
Tests are run with [tox](https://tox.readthedocs.io/en/latest/) against python 3.9. 

From the root directory of the project, simply call:
```bash
tox
```

## Roadmap
### V1
Commands to add:
* `flask generate model`: generate a Flask-SQLAlchemy model, a new test file, and Flask-Marshmallow schema.
* `flask generate form`: generates a Flask-WTF form, and imports it to the `forms/__init__.py` file. 
* `flask generate stylesheet`: generates a new .scss stylesheet and imports it to the `assets/stylesheets/styles.scss` file. 
* `flask install uploads`: install Flask-Uploads
* `flask install babel`: install Flask-Babel
* `flask install login`: install Flask-Login
* `flask install mail`: install Flask-Mail
* `flask install talisman`: install Flask-Talisman
* `flask isntall cors`: install Flask-CORS
* `flask install security`: install Flask-Security
* `flask install restful`: install Flask-Restful

Wrap `flask build` and `flask watch` commands in a `flask webpack [COMMAND]` command group. 

Allow skipping of webpack, and using a simple 'static' folder. 



* Add an `--api` option to the `new` command to install `Flask-Restful` and `Marshmallow` and generate a blueprint for API resources.
* Add an `--spa` option to the `new` command to set up a Node JS project and generate a "catch all" client blueprint for rendering a JS Single Page Application (SPA). Possibly integrate with `create-react-app` and/or Vue's hello world example.
* Add a `--websocket` option to the `new` command to install `Flask-SocketIO` and use its event loop instead of standard flask server.
* Add a `--skip-db` option to the `new` command to not install SQLAlchemy.
* Implement a flexible uploads system that can be configured to work with multiple back ends
* ...and more