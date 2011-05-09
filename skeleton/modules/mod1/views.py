from flask import render_template
from mod1 import module

@module.route('/mod1_view')
def index(name = None):
    return render_template('mod1/mod1_view.html', name = name)
