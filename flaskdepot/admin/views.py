from flask import Blueprint, abort, flash, render_template, current_app, request
from flask.ext.login import login_required, current_user
from sqlalchemy import func
from flaskdepot.admin.controllers import AdminAccountEditForm
from flaskdepot.extensions import db
from flaskdepot.file.models import Download, File, Vote, Comment
from flaskdepot.user.models import User, Usergroup
from flaskdepot.utils.helper import likeable

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
@admin.route('/user/<int:page>', methods=['GET'])
@login_required
def user(page=1):
    users = User.query
    _username = request.args.get('username')
    _email = request.args.get('email')
    _usergroup = request.args.get('usergroup')

    if _username and len(_username) > 0:
        users = users.filter(User.username.ilike(likeable(_username)))
    if _email and len(_email) > 0:
        users = users.filter(User.email.ilike(likeable(_email)))
    if _usergroup and len(_usergroup) > 0:
        users = users.filter(User.group_id.is_(_usergroup))

    users = users.paginate(page, current_app.config['RESULTS_PER_PAGE'], False)
    usergroups = Usergroup.query.all()
    return render_template('admin/user.html', users=users, usergroups=usergroups, title="User administration")


@admin.route('/file', methods=['GET'])
@admin.route('/file/<int:page>', methods=['GET'])
@login_required
def file(page=1):
    files = File.query
    _filename = request.args.get('filename')
    _author = request.args.get('author')

    if _filename and len(_filename) > 0:
        files = files.filter(File.file_name.ilike(likeable(_filename)))
    if _author and len(_author) > 0:
        files = files.filter(File.author_id.is_(_author))

    files = files.paginate(page, current_app.config['RESULTS_PER_PAGE'], False)
    users = db.session.query(User)\
        .join(Usergroup)\
        .filter(Usergroup.is_uploader)\
        .filter(User.group_id == Usergroup.id)\
        .all()
    return render_template('admin/file.html', files=files, users=users, title="File administration")


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