*\~work in progress\~*

# Flask-Boot

An opinionated command line tool for bootstrapping Flask applications with less boiler-plate code.

Inspired by Ruby on Rails.


## Installing
This has not been deployed to PYPI yet, as it is still under active development. 

To install, clone the repo and install using pip 
```bash
git clone git@github.com:graydenshand/flask_boot.git
pip install ./flask_boot # path to source code
```

## Usage
Currently there are just two commands:
```bash
flask_boot new <name>
flask_boot destroy <name>
```
The `new` command creates a Flask app in a new directory with the specified name.

The `destroy` command will recursively erase a directory with the specified name. Be careful with this, as it will erase any directory you specify without checking to make sure it's actually a Flask-Boot project. 

## Roadmap
* Finish building the basic template. Add SQLAlchemy (Flask-SQLAlchemy) + Alembic (Flask-Migrate). 
* Extend Flask's CLI with a set of commands for quickly generating and destroying assets. E.g. `flask g route login` might generate a view function, map it to a url, generate a template, and generate a test.
* Add an `install` command for installing common flask extensions.
* Add an `--api` option to the `new` command to install `Flask-Restful` and `Marshmallow` and generate a blueprint for API resources.
* Add an `--spa` option to the `new` command to set up a Node JS project and generate a "catch all" client blueprint for rendering a JS Single Page Application (SPA). Possibly integrate with `create-react-app` and/or Vue's hello world example.
* Add a `--websocket` option to the `new` command to install `Flask-SocketIO` and use its event loop instead of standard flask server.
* Add a `--skip-db` option to the `new` command to not install SQLAlchemy.
* ...and more