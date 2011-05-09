from flask import render_template
from mod2 import module

@module.route('/')
def index():
    return render_template('mod2/index.html')
