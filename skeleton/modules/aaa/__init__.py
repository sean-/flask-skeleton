# -*- coding: utf-8 -*-
import base64, hashlib, M2Crypto
from functools import wraps

from flask import current_app, flash, g, Markup, Module, redirect, request, session, url_for

module = Module(__name__, 'aaa')

LOGIN_SUFFIX_BLACKLIST = {
    '/logout': True,
    '/login': True
}


def gen_session_id():
    """ Generates a session ID """
    # Be kind to future support people and developers by using a base32
    # encoded session id. Why is this cool? Read RFC3548 §5 and rejoice
    # at the lack of ambiguity regarding "one", "ell", "zero" and
    # "ohh". You can thank me later.
    return base64.b32encode(M2Crypto.m2.rand_bytes(current_app.config['SESSION_BYTES']))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'li' not in session:
            session['dsturl'] = request.path
            flash('Login required for previous page')
            return redirect(url_for('aaa.login'))
        return f(*args, **kwargs)
    return decorated_function


def fresh_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'li' not in session:
            session['dsturl'] = request.path
            flash('Fresh login required for previous page')
            return redirect(url_for('aaa.login'))
        return f(*args, **kwargs)
    return decorated_function
