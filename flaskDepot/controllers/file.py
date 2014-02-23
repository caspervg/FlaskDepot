from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms import TextField, TextAreaField, SelectField, Form, IntegerField
from wtforms.validators import Required, NumberRange, Length, Optional
from flaskDepot import app
from flaskDepot.controllers.base import RedirectForm
from flaskDepot.models import File


class UploadForm(RedirectForm):

    filename = TextField('Filename', validators=[
        Required("Please enter a file name.")]
    )
    package = FileField('File', validators=[
        FileRequired(message="Please select a file to upload."),
        FileAllowed(app.config['FILE_EXTENSIONS'], message="You can only upload compressed (.zip, .rar) files.")])

    image_1 = FileField('Preview 1', validators=[
        FileRequired(message="Please select a preview image to upload."),
        FileAllowed(app.config['PREVIEW_EXTENSIONS'], message="You can only upload image (.png, .jpg, .gif) files.")
    ])

    image_2 = FileField('Preview 2', validators=[
        FileAllowed(app.config['PREVIEW_EXTENSIONS'], message="You can only upload image (.png, .jpg, .gif) files.")
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

        if self.package.data:
            other_file = File.query.filter_by(file_name=secure_filename(self.package.data.filename)).first()
            if other_file:
                self.package.errors.append('A package (.zip, .rar) with this name already exists.')
                validate = False

        for image in [self.image_1, self.image_2]:
            i_file = image.data
            if file is not None:
                o_file1 = File.query.filter_by(preview1_name=secure_filename(i_file.filename)).first()
                o_file2 = File.query.filter_by(preview2_name=secure_filename(i_file.filename)).first()
                if o_file1 or o_file2:
                    image.errors.append('A preview image with this name already exists.')
                    validate = False

        return validate


class EvaluationForm(RedirectForm):

    rating = IntegerField('Rating', validators=[Optional(), NumberRange(min=0, max=5)])
    comment = TextAreaField('Comment', validators=[Length(min=16, max=512)])