from flask import Blueprint, abort, flash, render_template
from flask.ext.login import login_required, current_user
from sqlalchemy import func
from flaskdepot.admin.controllers import AdminAccountEditForm
from flaskdepot.extensions import db
from flaskdepot.file.models import Download, File, Vote, Comment
from flaskdepot.user.models import User, Usergroup

admin = Blueprint("admin", __name__)

@admin.before_request
def check_admin():
    if not current_user.group.is_admin:
        abort(403)


@admin.route('/index', methods=['GET'])
@login_required
def index():
    stats = list()
    stats.append({
        'name': 'Downloads',
        'result': db.session.query(func.count(Download.id)).scalar()
    })
    stats.append({
        'name': 'Files',
        'result': db.session.query(func.count(File.id)).scalar()
    })
    stats.append({
        'name': 'Users',
        'result': db.session.query(func.count(User.id)).scalar()
    })
    stats.append({
        'name': 'Votes',
        'result': db.session.query(func.count(Vote.id)).scalar()
    })
    stats.append({
        'name': 'Comments',
        'result': db.session.query(func.count(Comment.id)).scalar()
    })

    return render_template('admin/index.html', stats=stats, title="Administration")

@admin.route('/user', methods=['GET'])
@login_required
def user():
    users = User.query.filter_by(active=True).all()
    return render_template('admin/user.html', users=users, title="User administration")


@admin.route('/file', methods=['GET'])
@login_required
def file():
    files = File.query.all()
    return render_template('admin/file.html', files=files, title="File administration")


@admin.route('/category', methods=['GET'])
@login_required
def category():
    return 'Category admin'


@admin.route('/file/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_file(id):
    return 'Edit file'


@admin.route('/user/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    _user = User.query.filter_by(id=id).first()
    form = AdminAccountEditForm()
    form.group.choices = [(group.id, group.name) for group in Usergroup.query.order_by('name')]

    if form.validate_on_submit():
        if form.group.data and form.group.data is not _user.group.id:
            _user.group_id = form.group.data
            flash('The user group has been updated')
        if form.username.data:
            _user.username = form.username.data
            flash('The username has been updated')
        db.session.commit()
    else:
        form.group.data = _user.group_id

    return render_template('admin/user_edit.html',
                           form=form,
                           title=u"Edit account for {0}".format(_user.username),
                           user=_user)