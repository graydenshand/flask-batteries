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
* ✅ `flask new`: generate a new Flask-Batteries app
* ✅ `flask webpack build`: build static assets with Webpack
* ✅ `flask webpack watch`: build and watch static assets with Webpack
* ✅ `flask (un)install sqlalchemy`: (un)install Flask-SQLAlchemy
* ✅ `flask (un)install migrate`: (un)install Flask-Migrate
* ✅ `flask (un)install wtf`: (un)install Flask-WTF
* ❌ `flask (un)install uploads`: (un)install Flask-Uploads
* ❌ `flask (un)install babel`: (un)install Flask-Babel
* ❌ `flask (un)install login`: (un)install Flask-Login
* ❌ `flask (un)install mail`: (un)install Flask-Mail
* ❌ `flask (un)install talisman`: (un)install Flask-Talisman
* ❌ `flask (un)install cors`: (un)install Flask-CORS
* ❌ `flask (un)install security`: (un)install Flask-Security
* ❌ `flask (un)install restful`: (un)install Flask-Restful
* ✅ `flask generate/destroy route`: generate/destroy a route, template, and test
* ❌ `flask generate/destroy model`: generate/destroy a Flask-SQLAlchemy model, a new test file, and Flask-Marshmallow schema.
* ❌ `flask generate form`: generates a Flask-WTF form, and imports it to the `forms/__init__.py` file. 
* ❌ `flask generate stylesheet`: generates a new .scss stylesheet and imports it to the `assets/stylesheets/styles.scss` file. 

* ✅ Allow skipping of webpack, and using a simple 'static' folder. 
