from flaskdepot.extensions import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'fd_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(25), unique=True)

    group_id = db.Column(db.Integer, db.ForeignKey('fd_usergroups.id'), nullable=False)

    created_on = db.Column(db.DateTime, default=datetime.now())
    created_ip = db.Column(db.String(16))

    last_active_on = db.Column(db.DateTime)
    last_active_ip = db.Column(db.String(16))

    files = db.relationship('File', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    downloads = db.relationship('Download', backref='user', lazy='dynamic')
    votes = db.relationship('Vote', backref='user', lazy='dynamic')

    email = db.Column(db.Unicode(100))
    password_hash = db.Column(db.String(60))

    active = db.Column(db.Boolean, default=True)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def url(self):
        return u'/user/{0}'.format(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return u'{0}'.format(self.id)


class Usergroup(db.Model):
    __tablename__ = 'fd_usergroups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100))

    users = db.relationship('User', backref='group')

    is_default = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
