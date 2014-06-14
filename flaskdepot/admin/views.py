from flask import Blueprint, abort, flash, render_template
from flask.ext.login import login_required, current_user
from flaskdepot.admin.controllers import AdminAccountEditForm
from flaskdepot.extensions import db
from flaskdepot.user.models import User, Usergroup

admin = Blueprint("admin", __name__)


@admin.route('/user/<id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if not current_user.group.is_admin:
        abort(403)
    else:
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

        return render_template('admin_user_edit.html', form=form, title=u"Edit account for {0}".format(_user.username), user=_user)