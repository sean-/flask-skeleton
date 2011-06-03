import random

from flask import render_template, request
from mod1 import module
from mod1.models import H2

from skeleton import cache

@cache.memoize(timeout=10)
def random_func(useless_parameter):
    """ Cache a random number for 10 seconds """
    # Ignore the useless_parameter for this example
    return random.randrange(0, 100000)

@module.route('/mod1_view')
def index(name = None):
    # Call random_func() 10x times, twice.
    cached_values = []
    for i in range(0,10):
        cached_values.append(random_func(i))
    for i in range(0,10):
        cached_values.append(random_func(i))

    # There should be 10 unique values even though we appended twice to the
    # list.
    cached_values = list(set(cached_values))
    unique_values = len(cached_values)
    return render_template('mod1/mod1_view.html', name=name, cached_values=cached_values, unique_values=unique_values)

@module.route('/list_all')
def list_all():
    entries = H2.query.all()
    return render_template('mod1/list_all.html', entries=entries)

@module.route('/list_one')
def list_one():
    id = request.args.get('id', 1)
    entry = H2.query.filter_by(id=id).first_or_404()
    return render_template('mod1/list_one.html', entry=entry)
