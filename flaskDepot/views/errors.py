from flaskDepot import app
from flask import render_template


@app.errorhandler(401)
def unauthorized(e):
    return render_template("error.html", name=u'Unauthorized',
                           message=u'Sorry, but you need to log in to access this page'), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", name=u'Forbidden',
                           message=u'Sorry, but you do not have access to this page'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", name=u'Not Found',
                           message=u'Sorry, the page you were looking for could not be found'), 404


@app.errorhandler(410)
def gone(e):
    return render_template("error.html", name=u'Gone',
                           message=u'Sorry, the page you were looking for has been moved or can not be accessed'), 410


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", name=u'Server Error',
                           message=u'Sorry, the server encountered an error while processing your request. Please try '
                                   u'again later. If this problem persists, contact the administration')