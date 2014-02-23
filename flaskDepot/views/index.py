from flask import render_template, jsonify
from flaskDepot import app
from flaskDepot.models import File, Comment


@app.route('/index/', methods=['GET'])
def index():
    files = File.query.order_by(File.created_on).limit(3).all()
    comments = Comment.query.order_by(Comment.id).limit(10).all()
    return render_template('index.html', files=files, comments=comments, title='Index')