from flaskdepot import app


@app.route('/search/', methods=['GET'])
def search():
    return u'Welcome to the search page of {0}'.format(app.config['DEPOT_TITLE'])