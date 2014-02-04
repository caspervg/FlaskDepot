from flask import render_template, request, flash
from flask_login import login_user, login_required, current_user, logout_user, fresh_login_required
from flaskDepot import app, db
from flaskDepot.controllers.user import RegistrationForm, LoginForm, AccountEditForm, AdminAccountEditForm, \
    AccountDeleteForm
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
    if not (current_user.group.is_admin or current_user.id == id):
        return 'You cannot access this page'
    else:
        user = User.query.filter_by(id=id).first()
        return render_template('profile.html', user=user, title=u"Profile for {0}".format(user.username))


@login_required
@app.route('/user/<id>/edit/', methods=['GET', 'POST'])
def edit_user(id):
    if not (current_user.group.is_admin or current_user.id == id):
        return 'You cannot access this page'
    else:
        user = User.query.filter_by(id=id).first()
        form = AccountEditForm()

        if form.validate_on_submit():
            if form.email.data:
                user.email = form.email.data
                flash('The e-mail address has been updated')
            if form.password.data and (form.password.data == form.confirm_password.data):
                user.set_password(form.password.data)
                flash('The password has been updated')
            db.session.commit()

        return render_template('user_edit.html', form=form, title="Edit profile", user=user)

@login_required
@app.route('/admin/user/<id>/edit/', methods=['GET', 'POST'])
def admin_edit_user(id):
    if not current_user.group.is_admin:
        return 'You cannot access this page'
    else:
        user = User.query.filter_by(id=id).first()
        form = AdminAccountEditForm()
        form.group.choices = [(group.id, group.name) for group in Usergroup.query.order_by('name')]
        form.group.data = user.group_id

        if form.validate_on_submit():
            if form.group.data and form.group.data is not user.group.id:
                user.group_id = form.group.data
                flash('The user group has been updated')
            if form.username.data:
                user.username = form.username.data
                flash('The username has been updated')
            db.session.commit()

        return render_template('admin_user_edit.html', form=form, title="Edit account", user=user)

@login_required
@app.route('/user/<id>/delete/', methods=['DELETE'])
def delete_user(id):
    if not (current_user.group.is_admin or current_user.id == id):
        return 'You cannot access this page'
    else:
        user = User.query.filter_by(id=id).first()
        form = AccountDeleteForm()

        if form.validate_on_submit():
            if current_user.group.is_admin:
                if user.username == form.username.data:
                    user.active = False
                    db.session.commit()
                else:
                    form.username.errors.append('Please enter the correct username')
                    form.redirect()
            else:
                if user.username == form.username.data:
                    if user.check_password(form.password.data):
                        user.active = False
                        db.session.commit()
                    else:
                        form.password.errors.append('Username and password did not match')
                else:
                    form.username.errors.append('Please enter the correct username')
                    form.redirect()

        return render_template('user_delete.html', form=form, title="Delete account", user=user)



@login_required
@app.route('/user/me/', methods=['GET'])
def user_me():
    return user_one(current_user.id)