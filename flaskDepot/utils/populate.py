import datetime
from flaskdepot.extensions import db
from flaskdepot.file.models import BroadCategory, NarrowCategory, File, Comment, Download, Vote
from flaskdepot.user.models import Usergroup, User


def create_default_groups():
    banned = Usergroup(name=u'Banned', is_banned=True)
    db.session.add(banned)

    member = Usergroup(name=u'Member', is_default=True)
    db.session.add(member)

    admin = Usergroup(name=u'Admin', is_admin=True)
    db.session.add(admin)

    guest = Usergroup(name=u'Guest')
    db.session.add(guest)
    db.session.commit()


def create_admin_user(username, password, email):
    admin_group = Usergroup.query.filter_by(is_admin=True).first()
    user_1 = User(username=username, group=admin_group)
    user_1.email = email
    user_1.set_password(password)
    db.session.add(user_1)
    db.session.commit()


def create_normal_user(username, password, email):
    normal_group = Usergroup.query.filter_by(is_default=True).first()
    user_2 = User(username=username, group=normal_group)
    user_2.email = email
    user_2.set_password(password)
    db.session.add(user_2)
    db.session.commit()


def create_sample_data():
    broadcat = BroadCategory(name=u'TestBroadCategory')
    db.session.add(broadcat)

    db.session.commit()

    narrwcat = NarrowCategory(name=u'TestNarrowCategory')
    broadcat.narrow_categories = [narrwcat]
    db.session.add(narrwcat)

    db.session.commit()

    user_1 = User.query.filter_by(is_admin=True).first()
    user_2 = User.query.filter_by(is_default=True).first()

    file = File(name=u'TestFile', description=u'A test file', version=u'1.0', author=user_2,
                num_views=3, file_name='MyTestFile.zip', preview1_name='MyPrev.png', preview2_name='MyPrev.gif',
                broad_category=broadcat, narrow_category=narrwcat)
    db.session.add(file)

    db.session.commit()

    comment = Comment(text=u'Some nice comment text. We love you!', file=file, user=user_1)
    db.session.add(comment)

    dl_1 = Download(last_downloaded=datetime.datetime.utcnow(), file=file, user=user_1)
    dl_2 = Download(last_downloaded=datetime.datetime.utcnow(), file=file, user=user_2)
    db.session.add(dl_1)
    db.session.add(dl_2)

    vote_1 = Vote(value=-3, file=file, user=user_1)
    vote_2 = Vote(value=7, file=file, user=user_2)
    vote_3 = Vote(value=-2, file=file, user=user_1)
    db.session.add(vote_1)
    db.session.add(vote_2)
    db.session.add(vote_3)

    db.session.commit()