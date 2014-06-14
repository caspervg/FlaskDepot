from wtforms import SelectField, TextField, Form
from flaskdepot.base.controllers import RedirectForm
from flaskdepot.user.models import User


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