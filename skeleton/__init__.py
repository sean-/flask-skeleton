from flask import Flask
from flaskext.csrf import csrf
from flaskext.sqlalchemy import SQLAlchemy

import os
import sys

__all__ = ['create_app','db']

# A list of app modules and their prefixes. Each APP entry must contain a
# 'name'.
#
# Models are always loaded at the time an app is loaded. Models are not used
# to automatically generate schema in this setup. After several apps and
# having iterated many times with SQLAlchemy to get the resulting schema
# "just right," I finally realized that SQL is the right dialect to describe
# your database's structure. Said differently, why use SQLAlchemy to describe
# what PostgreSQL already does infinitely better? Use SQLAlchemy for what it
# is especially good at: generating efficient SQL based on mappings between
# Python classes and database tables. A few extra lines of code in the
# various models goes a long ways towards clarity, predictability and
# explicitness.
#
# Re: PostgreSQL vs other RDBMS'es. Portability to other relational databases
# is not something I design for. PostgreSQL is faster, more stable, the most
# standards conformant relational database and is rediculously feature
# rich. Based purely on its technical merrits, the only two situations where
# I would use a different relational database would be if my target hosting
# platform did not support SystemV shared memory or was an embedded
# device. Hell will have frozen over if MySQL, Oracle, DB2 or MS-SQL actually
# produce a compelling reason to use their technology over PostgreSQL.
MODULES = [
#   {'name': 'foo',  'url_prefix': '/admin', 'models': ['Topic']   },
    {'name': 'home', 'url_prefix': '/',      'models': ['h1','h3'] },
    {'name': 'mod1', 'url_prefix': '/',      'models': ['h2'],     },
    {'name': 'mod2', 'url_prefix': '/mod2'                         },
    {'name': 'mod3', 'url_prefix': '/mod3'                         },
]

# models are added to the db's metadata when create_app() is actually called.
db = SQLAlchemy()

# Create the Skeleton app
def create_app(name = __name__):
    app = Flask(__name__, static_path='/static')
    app.config.from_object(__name__)
    app.config.from_object('default_settings')
    app.config.from_envvar('SKELETON_SETTINGS', silent=True)

    # Init the database engine
    db.init_app(app)

    cur = os.path.abspath(__file__)
    sys.path.append(os.path.dirname(cur) + '/modules')
    for m in MODULES:
        mod_name = '%s.views' % m['name']
        views = __import__(mod_name)
        url_prefix = None
        if m.has_key('url_prefix'):
            url_prefix = m['url_prefix']

        if app.config['DEBUG']:
            print '[VIEW ] Mapping views in %s to prefix: %s' % (mod_name, url_prefix)

        # Automatically map '/' to None to prevent modules from stepping on
        # one another.
        if url_prefix == '/':
            url_prefix = None
        load_module_models(app, m)
        app.register_module(views.module, url_prefix=url_prefix)

    # csrf protect the app
    csrf(app)
    return app

# Load a module's models
def load_module_models(app, module):
    if not module.has_key('models'):
        return

    for model in module['models']:
        model_name = '%s.models.%s' % (module['name'], model)
        if app.config['DEBUG']:
            print '[MODEL] Loading db model %s' % (model_name)
        mod = __import__(model_name)
