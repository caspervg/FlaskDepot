from flaskDepot import app, db
from flaskDepot.models import User, Usergroup
from flaskDepot.views.base import RedirectForm, get_redirect_target
from flask import render_template, request, session, flash
from flask.ext.classy import FlaskView
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Length, EqualTo, Email


# User Registration
class RegistrationForm(RedirectForm):
    username = TextField('Username', validators=[Required()])

    email = TextField('E-mail', validators=[Required(), Email()])
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


class RegisterView(FlaskView):

    def index(self):
        form = RegistrationForm()
        return render_template('register.html', form=form)

    def post(self):
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

            session['user_id'] = user.id
            flash(u'Thank you for signing up! You are now logged in as {0}'.format(user.username))

            return form.redirect()
        else:
            return render_template('register.html', form=form)

RegisterView.register(app)


# User Sign-in
class LoginForm(RedirectForm):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

    def __init__(self, *args, **kwargs):
        RedirectForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        validate = Form.validate(self)

        if not validate:
            return False

        if self.username.data:
            user = User.query.filter(db.func.lower(User.username) == db.func.lower(self.username.data)).first()
            if not user:
                self.username.errors.append('No user with that username exists.'
                                            ' Make sure that you have typed it correctly')
                return False
            if not user.check_password(self.password.data):
                self.password.errors.append('The password you have used is incorrect.'
                                            ' Make sure that you have typed it correctly')
                return False

            self.user = user
            return True


class LoginView(FlaskView):

    def index(self):
        form = LoginForm()
        return render_template('login.html', form=form)

    def post(self):
        form = LoginForm()

        if form.validate_on_submit():
            session['user_id'] = form.user.id
            flash(u'You have been logged in as {0}'.format(form.user.username))
            return form.redirect('/')
        else:
            return render_template('login.html', form=form)

LoginView.register(app)