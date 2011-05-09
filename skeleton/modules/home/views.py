from flask import render_template
from home import module

@module.route('/')
def index(name = None):
    return render_template('home/index.html', name = name)
