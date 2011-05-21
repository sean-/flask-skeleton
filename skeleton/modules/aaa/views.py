from flask import flash, redirect, render_template, request, session, url_for
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
#        user = User(form.email.data, form.password.data)
#        db_session.add(user)
        flash('Thanks for registering, %s' % (form.email.data))
        return redirect(url_for('aaa.login'))
    return render_template('aaa/register.html', form=form)
