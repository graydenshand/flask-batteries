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
* Finish building the basic template. Add SQLAlchemy (Flask-SQLAlchemy) + Alembic (Flask-Migrate). 
* Extend Flask's CLI with a set of commands for quickly generating and destroying assets. E.g. `flask g route login` might generate a view function, map it to a url, generate a template, and generate a test.
* Add an `install` command for installing common flask extensions.
* Add an `--api` option to the `new` command to install `Flask-Restful` and `Marshmallow` and generate a blueprint for API resources.
* Add an `--spa` option to the `new` command to set up a Node JS project and generate a "catch all" client blueprint for rendering a JS Single Page Application (SPA). Possibly integrate with `create-react-app` and/or Vue's hello world example.
* Add a `--websocket` option to the `new` command to install `Flask-SocketIO` and use its event loop instead of standard flask server.
* Add a `--skip-db` option to the `new` command to not install SQLAlchemy.
* Implement a flexible uploads system that can be configured to work with multiple back ends
* ...and more