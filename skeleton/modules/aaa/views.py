# -*- coding: utf-8 -*-
import base64, hashlib, M2Crypto

from flask import current_app, flash, redirect, render_template, request, session, url_for
from sqlalchemy.sql.expression import bindparam, text
from sqlalchemy.types import LargeBinary

from skeleton import db
from aaa.forms import LoginForm, RegisterForm
from aaa import module

def gen_session_id():
    """ Generates a session ID """
    # Be kind to future support people and developers by using a base32
    # encoded session id. Why is this cool? Read RFC3548 §5 and rejoice
    # at the lack of ambiguity regarding "one", "ell", "zero" and
    # "ohh". You can thank me later.
    return base64.b32encode(M2Crypto.m2.rand_bytes(current_app.config['SESSION_BYTES']))

@module.route('/login', methods=('GET','POST'))
def login():
    form = LoginForm()
    if not session.has_key('i'):
        session['i'] = gen_session_id()

    if form.validate_on_submit():
        remote_addr = request.environ['REMOTE_ADDR']

        # Hash the password once here:
        h = hashlib.new('sha256')
        h.update(current_app.config['PASSWORD_HASH'])
        h.update(form.password.data)
        shapass = h.digest()

        ses = db.session
        result = ses.execute(
            # SELECT result, "column", message FROM aaa.login(email := 'user@example.com', password := '\xbd\x18\xee\x85\x9f\x19Bl\x1e\x9dE\\xdc\x10\xe2NH\x1b\x94\xe5n\x01C\x98\xe5AQ\x05\xb2\xa7,\x1co', ip_address := '11.22.33.44', session_id := 'user session id from flask', renewal_interval := '60 minutes'::INTERVAL) AS (result BOOL, "column" TEXT, message TEXT);
            text("SELECT ret, col, msg FROM aaa.login(:email, :pw, :ip, :sid, :idle) AS (ret BOOL, col TEXT, msg TEXT)",
                 bindparams=[
                    bindparam('email', form.email.data),
                    bindparam('pw', shapass, type_=LargeBinary),
                    bindparam('ip', remote_addr),
                    bindparam('sid', session.sid),
                    bindparam('idle',form.idle_ttl.data)]))
        row = result.first()
        if row[0] == True:
            ses.commit()
            flash('Successfully logged in as %s' % (form.email.data))
            return redirect(url_for('home.index'))
        else:
            # Return a useful error message from the database
            try:
                field = form.__getattribute__(row[1])
                field.errors.append(row[2])
            except AttributeError as e:
                pass

        return redirect(url_for('home.index'))
    return render_template('aaa/login.html', form=form)


@module.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return render_template('aaa/logout.html')


@module.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm()
    if not session.has_key('i'):
        session['i'] = gen_session_id()

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
            ses.commit()
            flash('Thanks for registering, %s' % (form.email.data))
            return redirect(url_for('aaa.login'))
        else:
            # Return a useful error message from the database
            try:
                field = form.__getattribute__(row[1])
                field.errors.append(row[2])
            except AttributeError as e:
                pass
    return render_template('aaa/register.html', form=form)
