from flask import flash, redirect, render_template, request, session, url_for
from sqlalchemy.sql.expression import bindparam, text

from skeleton import db
from aaa.forms import LoginForm, RegisterForm
from aaa import module

@module.route('/login', methods=('GET','POST'))
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session['logged_in'] = True
        flash('Logged in Successfully')
        return redirect(url_for('home.index'))
    return render_template('aaa/login.html', form=login_form)


@module.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return render_template('aaa/logout.html')


@module.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        remote_addr = request.environ['REMOTE_ADDR']
        # Form validates, execute the registration pl function
        ses = db.session
        result = ses.execute(
            text("SELECT ret, col, msg FROM aaa.register(:email, :pw, :ip) AS (ret BOOL, col TEXT, msg TEXT)", bindparams=[
                    bindparam('email', form.email.data),
                    bindparam('pw', form.password.data),
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
