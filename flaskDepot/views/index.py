from flaskDepot import app


@app.route('/index/', methods=['GET'])
def index():
    return u'Welcome to the {0}'.format(app.config['DEPOT_TITLE'])