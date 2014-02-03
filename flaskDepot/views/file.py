from datetime import datetime
import hashlib
import os
from flask.ext.login import current_user, login_required
from werkzeug.debug.repr import dump
from werkzeug.utils import secure_filename
from flaskdepot import app, db
from flaskdepot.models import User, Usergroup, File, BroadCategory, NarrowCategory
from flaskdepot.views.base import RedirectForm, get_redirect_target
from flask import render_template, request, session, flash, jsonify
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Required

class UploadForm(Form):

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

            for i_file in [self.image_1.data, self.image_2.data]:
                if file is not None:
                    o_file1 = File.query.filter_by(preview1_name=secure_filename(i_file.filename)).first()
                    o_file2 = File.query.filter_by(preview2_name=secure_filename(i_file.filename)).first()
                    if o_file1 or o_file2:
                        i_file.errors.append('A preview image with this name already exists.')
                        validate = False

            return validate


@login_required
@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    form.broad_category.choices = [(cat.id, cat.name) for cat in BroadCategory.query.order_by('name')]
    form.narrow_category.choices = [(cat.id, cat.name) for cat in NarrowCategory.query.order_by('name')]

    if form.validate_on_submit():
        new_file = File()
        new_file.name = form.filename.data
        new_file.file_name = secure_filename(form.package.data.filename)
        new_file.preview1_name = secure_filename(form.image_1.data.filename)
        new_file.preview2_name = secure_filename(form.image_2.data.filename) or None
        new_file.description = form.description.data
        new_file.version = form.version.data
        new_file.broad_category = form.broad_category.data
        new_file.narrow_category = form.narrow_category.data
        new_file.author_id = current_user.id

        package = form.package.data
        package.save(os.path.join(app.config['FILE_DIR'], secure_filename(package.filename)))

        prev1 = form.image_1.data
        prev1.save(os.path.join(app.config['PREVIEW_DIR'], secure_filename(prev1.filename)))

        if form.image_2.data.filename is not None:
            prev2 = form.image_2.data
            prev2.save(os.path.join(app.config['PREVIEW_DIR'], secure_filename(prev2.filename)))

        db.session.add(new_file)
        db.session.commit()

        flash('uploading succeeded')
        return "ok"

    return render_template('upload.html', form=form)