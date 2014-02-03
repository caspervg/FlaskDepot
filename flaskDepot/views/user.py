from wtforms.fields.html5 import EmailField
from flaskdepot import app, db
from flaskdepot.models import User, Usergroup
from flaskdepot.views.base import RedirectForm, get_redirect_target
from flask import render_template, request, session, flash, jsonify, url_for
from flask_wtf import Form
from flask_login import login_user, login_required, current_user
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Length, EqualTo, Email
from flask.ext import login
# testing


# User Registration
class RegistrationForm(RedirectForm):
    username = TextField('Username', validators=[Required()])

    email = EmailField('E-mail', validators=[Required(), Email()])
    confirm_email = TextField('Confirm E-mail', validators=[
        Required(),
        EqualTo('email', message="The two e-mails you entered must match")
    ])

    password = PasswordField('Password', validators=[Required(), Length(4,64)])
    confirm_password = PasswordField('Confirm Password', validators=[
        Required(),
        EqualTo('password', message='The two passwords you entered must match')
    ])

    def validate(self):
        validate = Form.validate(self)

        if not validate:
            return False

        if self.username.data:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                self.username.errors.append('An account already exists with that username')
                return False

        return validate


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


# User Login
class LoginForm(RedirectForm):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

    def validate(self):
        validate = Form.validate(self)

        if not validate:
            return False

        if self.username.data:
            user = User.query.filter(db.func.lower(User.username) == db.func.lower(self.username.data)).first()
            if not user:
                self.username.errors.append('No user with that username exists.'
                                            ' Make sure that you have typed it correctly.')
                return False
            if not user.check_password(self.password.data):
                self.password.errors.append('The password you have used is incorrect.'
                                            ' Make sure that you have typed it correctly.')
                return False
            return True


@app.route('/login/', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.user)
        flash(u'You have been logged in as {0}'.format(form.user.username))
        return form.redirect()
    else:
        return render_template('login.html', form=form)

# User Profile
@login_required
@app.route('/user/all', methods=['GET'])
def user_index():
    if current_user.group.is_admin:
        users = User.query.all()
        ret = ''
        for user in users:
            ret += '{0}<br>'.format(user.username)
        return ret
    else:
        return 'You cannot access this page'

@login_required
@app.route('/user/<id>', methods=['GET'])
def user_one(id):
    if current_user.group.is_admin:
        user = User.query.filter(User.id == id).first()
        return user.username
    else:
        return 'You cannot access this page'

@login_required
@app.route('/user/me', methods=['GET'])
def user_me():
    return current_user.username


# Flask-Login initialisation
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

init_login()