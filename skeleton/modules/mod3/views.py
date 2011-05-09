from flask import render_template
from mod3 import module

@module.route('/')
def some_random_view():
    return render_template('mod3/root.html')
