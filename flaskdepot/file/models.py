from datetime import datetime
from flaskdepot.extensions import db


class BroadCategory(db.Model):
    __tablename__ = 'broadcategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), unique=True)

    description = db.Column(db.UnicodeText)
    files = db.relationship('File', backref='broad_category', lazy='dynamic')

    @property
    def url(self):
        return u'/category/broad/{0}'.format(self.id)


class NarrowCategory(db.Model):
    __tablename__ = 'narrowcategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), unique=True)

    description = db.Column(db.UnicodeText)
    files = db.relationship('File', backref='narrow_category', lazy='dynamic')

    @property
    def url(self):
        return u'/category/narrow/{0}'.format(self.id)


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(128), unique=True)

    description = db.Column(db.UnicodeText)
    version = db.Column(db.Unicode(20))

    author_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    is_locked = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)

    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime)

    num_downloads = db.Column(db.Integer)
    num_views = db.Column(db.Integer)

    dependencies = db.Column(db.UnicodeText)

    comments = db.relationship('Comment', backref='file', lazy='dynamic')
    downloads = db.relationship('Download', backref='file', lazy='dynamic')
    votes = db.relationship('Vote', backref='file', lazy='dynamic')

    broad_category_id = db.Column(db.Integer, db.ForeignKey('broadcategory.id'), nullable=False)
    narrow_category_id = db.Column(db.Integer, db.ForeignKey('narrowcategory.id'), nullable=False)

    file_name = db.Column(db.String(128))
    slug = db.Column(db.String(128))
    preview1_name = db.Column(db.String(128))
    preview2_name = db.Column(db.String(128))

    @property
    def url(self):
        return u'/file/{0}'.format(self.id)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText)
    #on = db.Column(db.DateTime, default=datetime.datetime.now)

    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


class Vote(db.Model):
    __tablename__ = 'vote'
    __tableargs__ = (db.UniqueConstraint('file_id', 'user_id'),
                     db.CheckConstraint('value > -1'),
                     db.CheckConstraint('value < 6'),
                     {})

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


class Download(db.Model):
    __tablename__ = 'download'

    id = db.Column(db.Integer, primary_key=True)

    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    num_downloaded = db.Column(db.Integer)
    last_downloaded = db.Column(db.DateTime)