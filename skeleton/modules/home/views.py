from flask import render_template
from home import module

@module.route('/')
def index():
    return render_template('home/index.html')
