import os
import sys

import json

from flask import Flask
from flaskext.cache import Cache
from flaskext.debugtoolbar import DebugToolbarExtension
from flaskext.sqlalchemy import SQLAlchemy
from repoze.browserid.middleware import BrowserIdMiddleware
from werkzeug.contrib.securecookie import SecureCookie

import filters

__all__ = ['create_app','db']

# A list of app modules and their prefixes. Each APP entry must contain a
# 'name', the remaining arguments are optional. An optional 'models': False
# argument can be given to disable loading models for a given module.
MODULES = [
#   {'name': 'foo',  'url_prefix': '/admin' },
    {'name': 'aaa',  'url_prefix': '/'      },
    {'name': 'home', 'url_prefix': '/'      },
    {'name': 'mod1', 'url_prefix': '/'      },
    {'name': 'mod2', 'url_prefix': '/mod2'  },
    {'name': 'mod3', 'url_prefix': '/mod3'  },
]

# Create the Skeleton app
def create_app(name = __name__):
    app = Flask(__name__, static_path='/static')
    load_config(app)
    cache.init_app(app)
    db.init_app(app)
    filters.init_app(app)
    register_local_modules(app)

    app.wsgi_app = ProxyFixupHelper(app.wsgi_app)

    # Enable the DebugToolbar
    if app.config['DEBUG_TOOLBAR']:
        toolbar = DebugToolbarExtension(app)

    # Always attempt to set a BrowserId. At some point this will get used,
    # but let's start setting it now.
    app.wsgi_app = BrowserIdMiddleware(
        app.wsgi_app, secret_key=app.config['BROWSER_SECRET_KEY'],
        cookie_name='b', cookie_path='/',
        cookie_domain=None, cookie_lifetime=86400 * 365 * 10,
        cookie_secure=None, vary=())

    return app


def load_config(app):
    app.config.from_object(__name__)
    app.config.from_object('default_settings')
    app.config.from_envvar('SKELETON_SETTINGS', silent=True)


# Load the local modules
def load_module_models(app, module):
    if 'models' in module and module['models'] == False:
        return

    model_name = module['name']
    if app.config['DEBUG']:
        print '[MODEL] Loading db model %s' % (model_name)
    model_name = '%s.models' % (model_name)
    try:
        mod = __import__(model_name)
    except ImportError as e:
        import re
        if re.match(r'No module named ', e.message) == None:
            print '[MODEL] Unable to load the model for %s: %s' % (model_name, e.message)
        return False
    return True


def register_local_modules(app):
    cur = os.path.abspath(__file__)
    sys.path.append(os.path.dirname(cur) + '/modules')
    for m in MODULES:
        mod_name = '%s.views' % m['name']
        views = __import__(mod_name)
        url_prefix = None
        if 'url_prefix' in m:
            url_prefix = m['url_prefix']

        if app.config['DEBUG']:
            print '[VIEW ] Mapping views in %s to prefix: %s' % (mod_name, url_prefix)

        # Automatically map '/' to None to prevent modules from stepping on
        # one another.
        if url_prefix == '/':
            url_prefix = None
        load_module_models(app, m)
        app.register_module(views.module, url_prefix=url_prefix)


# Seeing 127.0.0.1 is almost never correct, promise.  We're proxied 99.9% of
# the time behind a load balancer or proxying webserver. Pull the right IP
# address from the correct HTTP header. In my hosting environments, I inject
# X-Real-IP as the HTTP header of choice instead of appending to
# X-Forwarded-For. Mixing and matching HTTP headers used by a client's proxy
# infrastructure and the server's infrastructure is almost always a bad idea.
class ProxyFixupHelper(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Only perform this fixup if the current remote host is localhost.
        if environ['REMOTE_ADDR'] == '127.0.0.1':
            host = environ.get('HTTP_X_REAL_IP', False)
            if host:
                environ['REMOTE_ADDR'] = host
        return self.app(environ, start_response)

# Cache
cache = Cache()

# SQL ORM Missive:
#
# Don't use models to automatically generate schemas. After iterating several
# times with SQLAlchemy (and nearly every other ORM from frameworks both long
# since dead and still trendy), to get a schema "just right" requires
# entirely too much fiddling in the ORM. My hard earned lesson: SQL is the
# right dialect to describe your database's structure (read: do not use an
# ORM to generate DDL). Other than portability, what's the advantage of
# describing your schema in SQLAlchemy?
#
# For as fantastic as SQLAlchemy is, using SQLAlchemy to generate schema is
# the equivalent of giving yourself a lobotomy while in the middle of
# attempting to write a Pulitzer Prize article. Why handicap yourself? Use
# SQLAlchemy for what it excels at: generating efficient SQL based on
# mappings between Python classes and database tables. Manually generated
# schema results in a few extra lines of code in a tiny number of files, but
# it goes a long ways towards clarity, predictability and
# explicitness. Automatic schema migrations, you say? l2dba or gtfo.
#
# Re: PostgreSQL vs other RDBMS'es. Here's another piece of hard earned
# knowledge from my last 14yrs of dorking with countless websites and
# databases: portability to other relational databases is a straw man
# argument. PostgreSQL is faster, more stable, the most standards conformant
# relational database, is ridiculously feature rich and cheaper to operate
# than its alternatives (both in terms of operations and efficiency on
# hardware), and that's the short list of reasons. If you are building a
# website, I am unable to produce a single fact based, data driven argument
# to use MySQL[1]. Hiring? Training?  Replication? Feh, that's FUD. Please
# stop perpetrating harm on your own organization and applications by
# succumbing to unfounded beliefs and lemmingism.
#
# [1] There are three situations where I would use a different relational
# database. The first two situations are: 1) if my target hosting platform
# did not support SystemV shared memory, or 2) I am architecting something
# for an embedded or mobile device. In the former case, I'd change hosting
# providers or would fire my system administrator, and in the latter, I'd use
# SQLite. What's the third case? The answer is DB2, but what's the question?

# Models are added to the db's metadata when create_app() is actually called.
db = SQLAlchemy()

# Heed SecureCookie.rst's warning and use json instead of pickle for
# serialization.
class JSONSecureCookie(SecureCookie):
    serialization_method = json
