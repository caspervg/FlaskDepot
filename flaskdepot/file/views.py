from datetime import datetime
import os
from flask import Blueprint, render_template, flash, abort, send_from_directory, current_app
from flask.ext.login import login_required, current_user
from slugify import slugify
from sqlalchemy import func
from werkzeug.exceptions import NotAcceptable, NotFound
from werkzeug.utils import secure_filename
from flaskdepot.extensions import db
from flaskdepot.file.controllers import UploadForm, EvaluationForm
from flaskdepot.file.models import BroadCategory, File, Comment, Vote, Download, NarrowCategory

file = Blueprint("file", __name__)


@file.route('/upload/', methods=['GET', 'POST'])
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

        # Create subdirectories for images and previews based on slug
        file_subdir = os.path.join(current_app.config['FILE_DIR'], new_file.slug)
        image_subdir = os.path.join(current_app.config['PREVIEW_DIR'], new_file.slug)
        if not os.path.exists(file_subdir):
            os.makedirs(file_subdir)
        if not os.path.exists(image_subdir):
            os.makedirs(image_subdir)

        form.package.data.save(os.path.join(file_subdir, new_file.file_name))

        prev1 = form.image_1.data
        prev1.save(os.path.join(image_subdir, new_file.preview1_name))

        if len(form.image_2.data.filename) is not 0:
            prev2 = form.image_2.data
            prev2.save(os.path.join(image_subdir, new_file.preview2_name))

        db.session.add(new_file)
        db.session.commit()

        flash('File has been uploaded')

    return render_template('file/upload.html', form=form, title="Upload")


@file.route('/<fileid>/<slug>/', methods=['GET', 'POST'])
@file.route('/<fileid>/', methods=['GET', 'POST'])
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

    _file = File.query.filter_by(id=fileid).first()

    if not _file:
        abort(404)

    allow_rating = not current_user.is_anonymous() and (Vote.query.filter_by(file_id=fileid, user_id=current_user.id).first() is None)
    num_rating = db.session.query(func.count(Vote.id)).filter_by(file_id=fileid).scalar()
    avg_rating = db.session.query(func.avg(Vote.value)).filter_by(file_id=fileid).scalar()

    return render_template('file/file.html',
                           upload=_file,
                           form=form,
                           allow_rating=allow_rating,
                           num_rating=num_rating,
                           avg_rating=avg_rating,
                           title=u'{0} by {1}'.format(_file.name, _file.author.username))


@file.route('/all/', methods=['GET'])
@login_required
def file_all():
    files = File.query.all()
    ret = ''
    for _file in files:
        ret += u'{0} by {1}<br>'.format(_file.name, _file.author.username)
    return ret


@file.route('/preview/<id>/<number>/')
def preview(id, number):
    _file = File.query.filter_by(id=id).first()
    if _file:
        if int(number) == 1:
            return send_from_directory(os.path.join(current_app.config['PREVIEW_DIR'], _file.slug), _file.preview1_name)
        elif int(number) == 2:
            if _file.preview2_name:
                return send_from_directory(os.path.join(current_app.config['PREVIEW_DIR'], _file.slug), _file.preview2_name)
            else:
                raise NotAcceptable()
        else:
            raise NotAcceptable()
    else:
        raise NotFound()


@login_required
@file.route('/package/<id>/')
def package(id):
    _file = File.query.filter_by(id=id).first()
    if _file:
        download = Download.query.filter_by(file_id=id, user_id=current_user.id).first()
        if download:
            download.last_downloaded = datetime.utcnow()
            download.num_downloaded += 1
            db.session.commit()
        else:
            download = Download()
            download.file = _file
            download.user = current_user
            download.num_downloaded = 1
            download.last_downloaded = datetime.utcnow()
            db.session.add(download)
            db.session.commit()

        return send_from_directory(os.path.join(current_app.config['FILE_DIR'], _file.slug), _file.file_name)
    else:
        raise NotFound()
