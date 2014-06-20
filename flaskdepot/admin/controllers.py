from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField, TextField, Form, TextAreaField
from wtforms.validators import Required
from flaskdepot.base.controllers import RedirectForm
from flaskdepot.file.models import File
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


class AdminFileEditForm(RedirectForm):
    fileid = -1
    filename = TextField('Filename', validators=[
        Required("Please enter a file name.")]
    )

    package = FileField('File', validators=[
        FileAllowed(['zip', 'rar'], message="You can only upload compressed (.zip, .rar) files.")])

    image_1 = FileField('Preview 1', validators=[
        FileAllowed(['png', 'jpg', 'gif'], message="You can only upload image (.png, .jpg, .gif) files.")
    ])

    image_2 = FileField('Preview 2', validators=[
        FileAllowed(['png', 'jpg', 'gif'], message="You can only upload image (.png, .jpg, .gif) files.")
    ])

    version = TextField('Version', default='1.0')

    description = TextAreaField('Description', validators=[
        Required("Please enter a description for your file.")
    ])

    broad_category = SelectField('Broad Category', coerce=int, validators=[
        Required("Please enter a broad category for your file.")
    ])

    narrow_category = SelectField('Narrow Category', coerce=int, validators=[
        Required("Please enter a narrow category for your file")
    ])

    def validate(self):
        validate = Form.validate(self)

        if self.filename.data:
            other_file = File.query.filter_by(name=self.filename.data).first()
            if other_file and other_file.id != int(self.fileid):
                self.filename.errors.append('A file with this name already exists.')
                validate = False

        return validate
