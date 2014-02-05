# User Login
from wtforms import TextField, PasswordField, Form, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Email, EqualTo, Length
from flaskDepot import db, app
from flaskDepot.controllers.base import RedirectForm
from flaskDepot.models import User
from flask.ext import login


class LoginForm(RedirectForm):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember Me')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

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

            self.user = user
            return True


# User Registration
class RegistrationForm(RedirectForm):
    username = TextField('Username', validators=[Required()])

    email = EmailField('E-mail', validators=[Required(), Email()])
    confirm_email = TextField('Confirm E-mail', validators=[
        Required(),
        EqualTo('email', message="The two e-mails you entered must match")
    ])

    password = PasswordField('Password', validators=[Required(), Length(4, 64)])
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


# User Edit Account
class AccountEditForm(RedirectForm):
    email = EmailField('E-mail', validators=[Email()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password', validators=[
        EqualTo('password', message='The two new passwords you entered must match')
    ])

    def validate(self):
        validate = Form.validate(self)

        if self.email.data:
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                self.email.errors.append('An account already exists with that e-mail')
                validate = False

        return validate


# User Delete Account
class AccountDeleteForm(RedirectForm):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Length(4, 64)])


# Admin Edit Account
class AdminAccountEditForm(RedirectForm):
    group = SelectField('User Group', coerce=int)
    username = TextField('Username')

    def validate(self):
        validate = Form.validate(self)

        if self.username.data:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                self.username.errors.append('An account already exists with that username')
                validate = False

        return validate


# Flask-Login initialisation
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

init_login()