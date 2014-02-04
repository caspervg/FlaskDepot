import os
from flask.ext.login import current_user, login_required
from werkzeug.utils import secure_filename
from flask import render_template, flash
from slugify import slugify
from flaskDepot import app, db
from flaskDepot.controllers.file import UploadForm
from flaskDepot.models import File, BroadCategory, NarrowCategory


@app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    form.broad_category.choices = [(cat.id, cat.name) for cat in BroadCategory.query.order_by('name')]
    form.narrow_category.choices = [(cat.id, cat.name) for cat in NarrowCategory.query.order_by('name')]

    if form.validate_on_submit():
        new_file = File()
        new_file.name = form.filename.data
        new_file.slug = slugify(form.filename.data)
        new_file.file_name = secure_filename(form.package.data.filename)
        new_file.preview1_name = secure_filename(form.image_1.data.filename)
        new_file.preview2_name = secure_filename(form.image_2.data.filename) or None
        new_file.description = form.description.data
        new_file.version = form.version.data
        new_file.broad_category_id = form.broad_category.data
        new_file.narrow_category_id = form.narrow_category.data
        new_file.author_id = current_user.id

        package = form.package.data
        package.save(os.path.join(app.config['FILE_DIR'], secure_filename(package.filename)))

        prev1 = form.image_1.data
        prev1.save(os.path.join(app.config['PREVIEW_DIR'], secure_filename(prev1.filename)))

        if len(form.image_2.data.filename) is not 0:
            prev2 = form.image_2.data
            prev2.save(os.path.join(app.config['PREVIEW_DIR'], secure_filename(prev2.filename)))

        db.session.add(new_file)
        db.session.commit()

        flash('File has been uploaded')

    return render_template('upload.html', form=form, title="Upload")


@app.route('/file/<fileid>/<slug>/', methods=['GET'])
@app.route('/file/<fileid>/', methods=['GET'])
def file_one(fileid, slug=None):
    upload = File.query.filter_by(id=fileid).first()
    return render_template('file.html', upload=upload)


@app.route('/file/all/', methods=['GET'])
@login_required
def file_all():
    files = File.query.all()
    ret = ''
    for afile in files:
        ret += u'{0} by {1}<br>'.format(afile.name, afile.author.username)
    return ret