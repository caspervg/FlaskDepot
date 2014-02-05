from flask import send_from_directory
from flask.ext.login import login_required
from werkzeug.exceptions import NotFound, NotAcceptable
from flaskDepot import app
from flaskDepot.models import File


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
    # TODO: Register a download for this file
    file = File.query.filter_by(id=id).first()
    return send_from_directory(app.config['FILE_DIR'], name)