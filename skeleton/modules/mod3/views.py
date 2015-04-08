# -*- coding:utf-8 -*-
from datetime import datetime

from flask import current_app, flash, redirect, render_template, \
    session, url_for
from flaskext.babel import to_user_timezone

from skeleton import babel, db
from aaa import login_required
from aaa.user import get_user_timezone

from . import module
from .forms import PageAddTagForm, PageSubmitForm
from .models import Page, PageTags, Tag


@babel.timezoneselector
def get_timezone():
    if 'li' in session:
        return get_user_timezone(session_id=session['i'])


@module.route('/')
def some_random_view():
    t = datetime.utcnow()
    return render_template('mod3/root.html', time=to_user_timezone(t))


@module.route('/pages')
def page_list():
    entries = Page.query.order_by(Page.url).all()
    return render_template('mod3/pages.html', pages=entries)

@module.route('/page/submit', methods=('GET','POST'))
@login_required
def page_submit():
    form = PageSubmitForm()
    if form.validate_on_submit():
        ses = db.session
        page = Page.query.filter_by(url = form.url.data.lower()).first()
        # Only add non-duplicate pages
        if page is None:
            page = Page(form.url.data)
            ses.add(page)
        ses.commit()
        return redirect(url_for('page_tags', page_id = page.id))
    return render_template('mod3/page_submit.html', form=form)


@module.route('/page/tags/<int:page_id>')
def page_tags(page_id):
    page = Page.query.filter_by(id = page_id).first_or_404()
    # Get a list of all of the tags that are on a given page. Note how we
    # created the join from the origin table, Tag, all the way over to the
    # Page table through the mapping table.
    tags = Tag.query.join(PageTags, Page).filter(Page.id == page.id).order_by('name').all()
    return render_template('mod3/page_tags.html', page=page, tags=tags)


@module.route('/tag/page/<int:page_id>/add', methods=('GET','POST'))
@login_required
def tag_add(page_id):
    page = Page.query.filter_by(id = page_id).first_or_404()
    form = PageAddTagForm()
    ses = db.session
    if form.validate_on_submit():
        # See if the tag already exists
        tag = Tag.query.filter_by(name = form.tag.data.lower()).first()
        if tag is None:
            # Create the tag
            tag = Tag(name = form.tag.data)
            ses.add(tag)
            flash('Adding tag %s' % tag.name)
        else:
            flash('Tag %s already exists with id %s, not adding' % (tag.name, tag.id))
        # See if there's a mapping row exists or not. If not, add one.
        if tag.pages.filter(Page.id == page.id).first() is None:
            tag.pages.append(page)
            flash('Adding tag %s to page %s' % (tag.name, page.url))
        else:
            flash('tag.id %s already exists for page %s' % (tag.id, page.id))
        ses.commit()
        return redirect(url_for('page_tags', page_id = page.id))
    return render_template('mod3/tag_add.html', form=form, page=page)


@module.route('/tag/pages/<int:tag_id>')
def tag_pages(tag_id):
    tag = Tag.query.filter_by(id = tag_id).first_or_404()
    return render_template('mod3/tag_pages.html', tag=tag)


@module.route('/tags')
def tag_list():
    tags = Tag.query.order_by('name').all()
    return render_template('mod3/tags.html', tags=tags)
