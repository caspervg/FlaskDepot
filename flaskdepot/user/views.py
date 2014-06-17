from flask import render_template, request, flash, url_for, redirect, Blueprint, abort
from flask_login import login_user, login_required, current_user, logout_user
from flaskdepot.extensions import db
from flaskdepot.user.models import User, Usergroup
from flaskdepot.user.controllers import RegistrationForm, LoginForm, AccountEditForm, AccountDeleteForm

user = Blueprint("user", __name__)


@user.route('/register/', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated():
        return redirect(url_for('base.index'))

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
        return render_template('user/register.html', form=form, title=u'Registration')


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form.next.data = url_for('base.index')

    if form.validate_on_submit():
        if not form.remember.data:
            login_user(form.user)
        else:
            login_user(form.user, remember=form.remember.data)

        flash(u'You have been logged in as {0}'.format(form.user.username))
        return form.redirect()
    else:
        return render_template('user/login.html', form=form, title=u'Log in')


@user.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(u'You have been logged out')
    return 'Logged out'


# User Profile
@user.route('/all/', methods=['GET'])
@login_required
def user_all():
    if current_user.group.is_admin:
        users = User.query.all()
        ret = ''
        for user in users:
            ret += u'{0}<br>'.format(user.username)
        return ret
    else:
        return 'You cannot access this page'


@user.route('/<id>/', methods=['GET'])
@login_required
def user_one(id):
    if current_user.group.is_admin or current_user.id == int(id):
        user = User.query.filter_by(id=id).first()
        return render_template('user/profile.html', user=user, title=u"Profile for {0}".format(user.username))
    else:
        return 'You cannot access this page'


@user.route('/<id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.group.is_admin or current_user.id == int(id):
        _user = User.query.filter_by(id=id).first()
        form = AccountEditForm()

        if form.validate_on_submit():
            if form.email.data:
                _user.email = form.email.data
                flash('The e-mail address has been updated')
            if form.password.data and (form.password.data == form.confirm_password.data):
                _user.set_password(form.password.data)
                flash('The password has been updated')
            db.session.commit()

        return render_template('user/edit.html', form=form, title=u"Edit profile for {0}".format(_user.username), user=_user)
    else:
        return 'You cannot access this page'


@user.route('/<id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    if not current_user.group.is_admin:
        abort(403)
    else:
        _user = User.query.filter_by(id=id).first()
        form = AccountDeleteForm()

        if form.validate_on_submit():
            if _user.username == form.username.data:
                _user.active = False
                db.session.commit()
            else:
                form.username.errors.append('Please enter the correct username')
                form.redirect()
        else:
            return render_template('user/delete.html', form=form,
                                   title=u"Delete account for {0}".format(_user.username), user=_user)


@user.route('/me/', methods=['GET'])
@login_required
def user_me():
    return user_one(current_user.id)