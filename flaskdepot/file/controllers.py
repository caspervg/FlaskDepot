from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms import TextField, TextAreaField, SelectField, Form, IntegerField
from wtforms.validators import Required, NumberRange, Length, Optional
from flaskdepot.base.controllers import RedirectForm
from flaskdepot.file.models import File


class UploadForm(RedirectForm):
    filename = TextField('Filename', validators=[
        Required("Please enter a file name.")]
    )
    package = FileField('File', validators=[
        FileRequired(message="Please select a file to upload."),
        FileAllowed(['zip', 'rar'], message="You can only upload compressed (.zip, .rar) files.")])

    image_1 = FileField('Preview 1', validators=[
        FileRequired(message="Please select a preview image to upload."),
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
            if other_file:
                self.filename.errors.append('A file with this name already exists.')
                validate = False

        return validate


class EditForm(RedirectForm):
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


class EvaluationForm(RedirectForm):
    rating = IntegerField('Rating', validators=[Optional(), NumberRange(min=0, max=5)])
    comment = TextAreaField('Comment', validators=[Length(min=16, max=512)])

