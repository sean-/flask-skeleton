from flask import render_template, request
from mod1 import module
from mod1.models import H2

@module.route('/mod1_view')
def index(name = None):
    return render_template('mod1/mod1_view.html', name=name)

@module.route('/list_all')
def list_all():
    entries = H2.query.all()
    return render_template('mod1/list_all.html', entries=entries)

@module.route('/list_one')
def list_one():
    id = request.args.get('id', 1)
    entry = H2.query.filter_by(id=id).first_or_404()
    return render_template('mod1/list_one.html', entry=entry)
