from flask import Flask
from flaskext.csrf import csrf

import os
import sys

# A list of app modules and their prefixes.
APPS = [
#    {'name': 'admin', 'url_prefix': '/admin', 'models': ['Topic'] },
    {'name': 'home', 'url_prefix': '/'},
    {'name': 'mod1',  'url_prefix': '/'},
    {'name': 'mod2',  'url_prefix': '/mod2'},
    {'name': 'mod3',  'url_prefix': '/mod3'},
]
DEFAULT_APP_NAME = 'skeleton'

# Create the Skeleton app
def create_app(app_name = DEFAULT_APP_NAME):
    app = Flask(app_name, static_path="/static")
    app.config.from_object(app_name)
    app.config.from_object('default_settings')
    app.config.from_envvar('SKELETON_SETTINGS', silent=True)

    cur = os.path.abspath(__file__)
    sys.path.append(os.path.dirname(cur) + '/modules')
    for a in APPS:
        mod_name = '%s.views' % a['name']
        views = __import__(mod_name)
        url_prefix = None
        if a.has_key('url_prefix'):
            url_prefix = a['url_prefix']

            # Automatically map '/' to None to prevent modules from stepping
            # on one another.
            if url_prefix == '/':
                url_prefix = None
        if app.config['DEBUG']:
            print "Registering mod %s to prefix %s" % (mod_name, url_prefix)
        app.register_module(views.module, url_prefix=url_prefix)
    csrf(app)
    return app

# create the Skeleton app. Reserve the app package variable so that the app
# can be imported easily. Nothing other than __main__ should call
# create_app().
app = create_app(__name__)
