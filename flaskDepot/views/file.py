import os
from flask.ext.login import current_user, login_required
from sqlalchemy import func
from werkzeug.exceptions import NotAcceptable
from werkzeug.utils import secure_filename
from flask import render_template, flash, url_for
from slugify import slugify
from flaskDepot import app, db
from flaskDepot.controllers.file import UploadForm, EvaluationForm
from flaskDepot.models import File, BroadCategory, NarrowCategory, Comment, Vote


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


@app.route('/file/<fileid>/<slug>/', methods=['GET', 'POST'])
@app.route('/file/<fileid>/', methods=['GET', 'POST'])
def file_one(fileid, slug=None):
    form = EvaluationForm()

    if form.validate_on_submit():
        if form.comment.data:
            comment = Comment()
            comment.text = form.comment.data
            comment.user_id = current_user.id
            comment.file_id = fileid
            db.session.add(comment)
            db.session.commit()
            flash(u'Your comment has been added', 'success')
    if form.rating.data:
        vote = Vote.query.filter_by(file_id=fileid, user_id=current_user.id).first()
        if not vote:
            vote = Vote()
            vote.value = form.rating.data
            vote.file_id = fileid
            vote.user_id = current_user.id
            db.session.add(vote)
            db.session.commit()
            flash(u'Your rating has been added', 'success')
        else:
            flash(u'You have already voted for this file', 'alert')

    upload = File.query.filter_by(id=fileid).first()
    allow_rating = not current_user.is_anonymous() and (Vote.query.filter_by(file_id=fileid, user_id=current_user.id).first() is None)
    num_rating = db.session.query(func.count(Vote.id)).filter_by(file_id=fileid).scalar()
    avg_rating = db.session.query(func.avg(Vote.value)).filter_by(file_id=fileid).scalar()

    return render_template('file.html',
                           upload=upload,
                           form=form,
                           allow_rating=allow_rating,
                           num_rating=num_rating,
                           avg_rating=avg_rating,
                           title=u'{0} by {1}'.format(upload.name, upload.author.username))


@app.route('/file/all/', methods=['GET'])
@login_required
def file_all():
    files = File.query.all()
    ret = ''
    for afile in files:
        ret += u'{0} by {1}<br>'.format(afile.name, afile.author.username)
    return ret