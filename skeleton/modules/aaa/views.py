import hashlib

from flask import current_app, flash, g, redirect, render_template, \
    request, session, url_for
from sqlalchemy.sql.expression import bindparam, text
from sqlalchemy.types import LargeBinary

from skeleton import db
from skeleton.lib import fixup_destination_url, local_request
from .forms import LoginForm, ProfileForm, RegisterForm
from . import fresh_login_required, gen_session_id, module
from skeleton.models import Timezone


@module.route('/login', methods=('GET','POST'))
def login():
    form = LoginForm()
    # Generate a session ID for them if they don't have one
    if 'i' not in session:
        session['i'] = gen_session_id()

    fixup_destination_url('dsturl','post_login_url')

    if form.validate_on_submit():
        remote_addr = request.environ['REMOTE_ADDR']

        # Hash the password once here:
        h = hashlib.new('sha256')
        h.update(current_app.config['PASSWORD_HASH'])
        h.update(form.password.data)
        shapass = h.digest()

        # Change out the values of the session ttl
        idle = '1 second'
        if form.idle_ttl.data == 'tmp':
            idle = '20 minutes'
        elif form.idle_ttl.data == 'day':
            idle = '1 day'
        elif form.idle_ttl.data == 'week':
            idle = '1 week'
        else:
            flask.abort(500)

        # Generate a new session ID upon login. If someone steals my session
        # id, I want to explicitly prevent its use as a way of inject
        # unauthenticated session information in to an authenticated
        # session. In the future once pgmemcache has been hooked up to the
        # database, the old session id will be expired from memcache
        # automatically.
        new_sess_id = gen_session_id()

        ses = db.session
        result = ses.execute(
            text("SELECT ret, col, msg FROM aaa.login(:email, :pw, :ip, :sid, :idle, :secure) AS (ret BOOL, col TEXT, msg TEXT)",
                 bindparams=[
                    bindparam('email', form.email.data),
                    bindparam('pw', shapass, type_=LargeBinary),
                    bindparam('ip', remote_addr),
                    bindparam('sid', new_sess_id),
                    bindparam('idle',idle),
                    bindparam('secure', request.is_secure)]))

        # Explicitly commit regardless of the remaining logic. The database
        # did the right thing behind the closed doors of aaa.login() and we
        # need to make sure that the logging to shadow.aaa_login_attempts is
        # COMMIT'ed so that customer support can help the poor, frustrated
        # (stupid?) users.
        ses.commit()
        row = result.first()
        if row[0] == True:
            session['i'] = new_sess_id
            session['li'] = True
            flash('Successfully logged in as %s' % (form.email.data))
            if 'post_login_url' in session:
                return redirect(session.pop('post_login_url'))
            else:
                return redirect(url_for('home.index'))
        else:
            session.pop('li', None)
            # Return a useful error message from the database
            try:
                # If the database says be vague, we'll be vague in our error
                # messages. When the database commands it we obey, got it?
                if row[1] == 'vague':
                    # Set bogus data so that 'form.errors == True'. If brute
                    # force weren't such an issue, we'd just append a field
                    # error like below. If you want to get the specifics of
                    # why the database rejected a user, temporarily change
                    # the above 'vague' to something that the database
                    # doesn't return, such as 'EDRAT' or something equally
                    # POSIXly funny.
                    form.errors['EPERM'] = 'There is no intro(2) error code for web errors'
                    pass
                else:
                    field = form.__getattribute__(row[1])
                    field.errors.append(row[2])
            except AttributeError as e:
                pass
    return render_template('aaa/login.html', form=form)


@module.route('/logout')
def logout():
    # Is there a destination post-logout?
    dsturl = None
    if request.referrer and local_request(request.referrer):
        dsturl = request.referrer
    else:
        dsturl = None

    # End the session in the database
    already_logged_out = False
    if 'li' in session:
        ses = db.session
        result = ses.execute(
            text("SELECT ret, col, msg FROM aaa.logout(:sid) AS (ret BOOL, col TEXT, msg TEXT)",
                 bindparams=[bindparam('sid', session['i'])]))
        ses.commit()
        # For now, don't test the result of the logout call. Regardless of
        # whether or not a user provides us with a valid session ID from the
        # wrong IP address, terminate the session. Shoot first, ask questions
        # later (i.e. why was a BadUser in posession of GoodUser's session
        # ID?!)
    else:
        already_logged_out = True

    # Nuke every key in the session
    for k in session.keys():
        session.pop(k)

    # Set a flash message after we nuke the keys in session
    if already_logged_out:
        flash('Session cleared for logged out user')
    else:
        flash('You were logged out')

    return render_template('aaa/logout.html', dsturl=dsturl)


@module.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm()
    if 'i' not in session:
        session['i'] = gen_session_id()

    form.timezone.query = Timezone.query.order_by(Timezone.name)
    if form.validate_on_submit():
        # Form validates, execute the registration pl function

        remote_addr = request.environ['REMOTE_ADDR']

        # Hash the password once here:
        h = hashlib.new('sha256')
        h.update(current_app.config['PASSWORD_HASH'])
        h.update(form.password.data)
        shapass = h.digest()

        ses = db.session
        result = ses.execute(
            text("SELECT ret, col, msg FROM aaa.register(:email, :pw, :ip) AS (ret BOOL, col TEXT, msg TEXT)",
                 bindparams=[
                    bindparam('email', form.email.data),
                    bindparam('pw', shapass, type_=LargeBinary),
                    bindparam('ip', remote_addr)]))
        row = result.first()
        if row[0] == True:
            # Update the user's timezone if they submitted a timezone
            if form.timezone.data:
                res = ses.execute(
                    text("INSERT INTO aaa.user_info (user_id, timezone_id) VALUES (get_user_id_by_email(:email), :tz)",
                         bindparams=[bindparam('email', form.email.data),
                                     bindparam('tz', form.timezone.data.id),]))
            ses.commit()
            flash('Thanks for registering! Please check your %s email account to confirm your email address.' % (form.email.data))
            return redirect(url_for('aaa.login'))
        else:
            # Return a useful error message from the database
            try:
                field = form.__getattribute__(row[1])
                field.errors.append(row[2])
            except AttributeError as e:
                pass
    return render_template('aaa/register.html', form=form)
