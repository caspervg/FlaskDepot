from datetime import datetime
from flask import send_from_directory
from flask.ext.login import login_required, current_user
from werkzeug.exceptions import NotFound, NotAcceptable
from flaskdepot import app, db
from flaskdepot.models import File, Download


@app.route('/preview/<id>/<number>/')
def preview(id, number):
    file = File.query.filter_by(id=id).first()
    if file:
        if int(number) == 1:
            return send_from_directory(app.config['PREVIEW_DIR'], file.preview1_name)
        elif int(number) == 2:
            if file.preview2_name:
                return send_from_directory(app.config['PREVIEW_DIR'], file.preview2_name)
            else:
                raise NotAcceptable()
        else:
            raise NotAcceptable()
    else:
        raise NotFound()


@login_required
@app.route('/package/<id>/')
def package(id):
    file = File.query.filter_by(id=id).first()
    if file:
        download = Download.query.filter_by(file_id=id, user_id=current_user.id).first()
        if download:
            download.last_downloaded = datetime.utcnow()
            download.num_downloaded += 1
            db.session.commit()
        else:
            download = Download()
            download.file = file
            download.user = current_user
            download.num_downloaded = 1
            download.last_downloaded = datetime.utcnow()
            db.session.add(download)
            db.session.commit()

        return send_from_directory(app.config['FILE_DIR'], file.file_name)
    else:
        raise NotFound()