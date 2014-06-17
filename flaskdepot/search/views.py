from flask import Blueprint, current_app

search = Blueprint("search", __name__)


@search.route('/', methods=['GET'])
def index():
    return u'Welcome to the search page of {0}'.format(current_app.config['DEPOT_TITLE'])