from flask import Blueprint, render_template
from flaskdepot.file.models import File, Comment

base = Blueprint("base", __name__)


@base.route('/')
@base.route('/index/', methods=['GET'])
def index():
    files = File.query.order_by(File.created_on).limit(3).all()
    comments = Comment.query.order_by(Comment.id).limit(10).all()
    return render_template('index.html', files=files, comments=comments, title='Index')