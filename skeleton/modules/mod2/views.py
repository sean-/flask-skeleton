# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

from flask import render_template, redirect, session, url_for

from skeleton import cache

from . import module

def user_logged_in():
    """ Returns true if the user is logged in """
    return True if 'li' in session else False

@module.route('/cache_logged_out')
@cache.cached(timeout=60, unless=user_logged_in)
def cache_logged_out():
    # Set a simple counter. A logged out user won't see this incrementing,
    # but a logged in user will.
    mc_key = 'user_page_count'
    count = cache.get(mc_key)
    if not count:
        count = 0
    cache.set(mc_key, count + 1)

    now = datetime.today()
    expires = now + timedelta(seconds = 60)

    return render_template('mod2/cache_logged_out.html', time=datetime.today(), expires=expires, count=count)

@module.route('/cached_always')
@cache.cached(timeout=15)
def cached_always():
    now = datetime.today()
    expires = now + timedelta(seconds = 15)
    return render_template('mod2/cached_always.html', time=now, expires=expires)

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
