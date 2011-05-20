from flask import render_template
from mod3 import module
from mod3.models import Page, Tag


@module.route('/')
def some_random_view():
    return render_template('mod3/root.html')


@module.route('/pages')
def page_list():
    entries = Page.query.all()
    return render_template('mod3/pages.html', pages=entries)


@module.route('/page/tags/<int:page_id>')
def page_tags(page_id):
    page = Page.query.filter_by(id = page_id).first_or_404()
    return render_template('mod3/page_tags.html', page=page)


@module.route('/tag/pages/<int:tag_id>')
def tag_pages(tag_id):
    tag = Tag.query.filter_by(id = tag_id).first_or_404()
    return render_template('mod3/tag_pages.html', tag=tag)


@module.route('/tags')
def tag_list():
    entries = Tag.query.all()
    return render_template('mod3/tags.html', tags=entries)
