from flask import render_template, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from flaskDepot import app, db
from flaskDepot.controllers.user import RegistrationForm, LoginForm
from flaskDepot.models import User, Usergroup


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)
        user.email = form.email.data
        user.created_ip = request.remote_addr
        user.group = Usergroup.query.filter_by(is_default=True).first()

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(u'Thank you for signing up! You are now logged in as {0}'.format(user.username))

        return form.redirect()
    else:
        return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.user)
        flash(u'You have been logged in as {0}'.format(form.user.username))
        return form.redirect()
    else:
        return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    flash(u'You have been logged out')
    return 'Logged out'


# User Profile
@login_required
@app.route('/user/all/', methods=['GET'])
def user_all():
    if current_user.group.is_admin:
        users = User.query.all()
        ret = ''
        for user in users:
            ret += u'{0}<br>'.format(user.username)
        return ret
    else:
        return 'You cannot access this page'


@login_required
@app.route('/user/<id>/', methods=['GET'])
def user_one(id):
    if current_user.group.is_admin:
        user = User.query.filter(User.id == id).first()
        return user.username
    else:
        return 'You cannot access this page'


@login_required
@app.route('/user/me/', methods=['GET'])
def user_me():
    return current_user.username