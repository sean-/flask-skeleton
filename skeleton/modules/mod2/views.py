from flask import render_template, redirect, url_for
from mod2 import module

@module.route('/')
def index():
    return render_template('mod2/index.html')

# Create a view that redirects to mod2's index: http://127.0.0.1:5000/mod2/redirect_here
@module.route('/redirect_here')
def redir_index():
    return redirect(url_for('index'))

# Create a view that redirects to home's index: http://127.0.0.1:5000/mod2/redirect_home
@module.route('/redirect_home')
def redir_index2():
    return redirect(url_for('home.index'))
