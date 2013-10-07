from flaskDepot import db, usergroup_cache, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class Config(db.Model):
    __tablename__ = 'fD_config'

    id = db.Column(db.Integer, primary_key=True)
    views = db.Column(db.Integer, default=0)


class Usergroup(db.Model):
    __tablename__ = 'fD_usergroups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100))

    users = db.relationship('User', backref='group')

    is_default = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    @classmethod
    def get_cached(cls, id):
        key = str(id)
        value = usergroup_cache.get(key)
        if value is None:
            value = cls.query.get(id)
            db.session.expunge(value)
            usergroup_cache.set(key, value)
        return value


class User(db.Model):
    __tablename__ = 'fD_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(25), unique=True)

    group_id = db.Column(db.Integer, db.ForeignKey('fD_usergroups.id'), nullable=False)

    created_on = db.Column(db.DateTime, default=datetime.datetime.now)
    created_ip = db.Column(db.String(16))

    last_active_on = db.Column(db.DateTime)
    last_active_ip = db.Column(db.String(16))

    files = db.relationship('File', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user_id', lazy='dynamic')
    downloads = db.relationship('Download', backref='user_id', lazy='dynamic')

    email = db.Column(db.Unicode(100))
    password_hash = db.Column(db.String(60))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def url(self):
        return u'/user/{0}'.format(self.id)

    @property
    def cached_group(self):
        return Usergroup.get_cached(self.group_id)


# (Narrow Category <-> Broad Category) Association
broad_narrow_association = db.Table('fD_broad_narrow_assocation', db.Model.metadata,
                                 db.Column('broad_id', db.Integer, db.ForeignKey('fD_broadcategories.id')),
                                 db.Column('narrow_id', db.Integer, db.ForeignKey('fD_narrowcategories.id')))


class BroadCategory(db.Model):
    __tablename__ = 'fD_broadcategories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), unique=True)

    description = db.Column(db.UnicodeText)

    narrow_categories = db.relationship('NarrowCategory', secondary=broad_narrow_association,
                                        backref="broad_category")

    @property
    def url(self):
        return u'/category/broad/{0}'.format(self.id)


class NarrowCategory(db.Model):
    __tablename__ = 'fD_narrowcategories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), unique=True)

    description = db.Column(db.UnicodeText)

    @property
    def url(self):
        return u'/category/narrow/{0}'.format(self.id)


class File(db.Model):
    __tablename__ = 'fD_files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), unique=True)

    description = db.Column(db.UnicodeText)
    version = db.Column(db.Unicode(20))

    creator_id = db.Column(db.Integer, db.ForeignKey('fD_users.id'), nullable=False)
    creator = db.relationship('User', uselist=False, primaryjoin='File.creator_id == User.id')

    is_locked = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)

    created_on = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_on = db.Column(db.DateTime)

    num_downloads = db.Column(db.Integer)
    num_views = db.Column(db.Integer)

    dependencies = db.Column(db.UnicodeText)

    comments = db.relationship('Comment', backref='file_id', lazy='dynamic')
    downloads = db.relationship('Download', backref='file_id', lazy='dynamic')

    file_name = db.Column(db.String(50))
    preview1_name = db.Column(db.String(50))
    preview2_name = db.Column(db.String(50))

    @property
    def url(self):
        return u'/file/{0}'.format(self.id)

    @property
    def edit_url(self):
        return url_for('edit_file',
                       thread_id=self.id)

    @property
    def delete_url(self):
        return url_for('delete_file',
                       thread_id=self.id)

    def can_be_edited_by(self, user):
        if user.is_admin:
            return True
        else:
            return user == self.creator

    def can_be_deleted_by(self, user):
        if user.is_admin:
            return True
        else:
            return user == self.creator


class Comment(db.Model):
    __tablename__ = 'fD_comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText)

    file = db.Column(db.Integer, db.ForeignKey('fD_files.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('fD_users.id'), nullable=False)


class Download(db.Model):
    __tablename__ = 'fD_downloads'

    id = db.Column(db.Integer, primary_key=True)

    file = db.Column(db.Integer, db.ForeignKey('fD_files.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('fD_users.id'), nullable=False)

    num_downloaded = db.Column(db.Integer)
    last_downloaded = db.Column(db.DateTime)