from flask import g, render_template
from mod1 import module
from mod1.models import H1

@module.route('/mod1_view')
def index(name = None):
    return render_template('mod1/mod1_view.html', name=name)

@module.route('/list')
def list():
    entries = H1.select().execute()
    return render_template('mod1/list.html', entries=entries)
